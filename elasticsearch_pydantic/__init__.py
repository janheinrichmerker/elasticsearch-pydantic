from datetime import datetime, date
from decimal import Decimal
from enum import Enum, IntEnum
from ipaddress import (
    IPv4Address,
    IPv6Address,
    IPv4Interface,
    IPv6Interface,
    IPv4Network,
    IPv6Network,
)
from pathlib import Path
from typing import (
    Literal,
    Annotated,
    Any,
    Sequence,
    Optional,
    Union,
    get_args,
    get_origin,
    Callable,
    Pattern,
    Tuple,
    Iterator,
)
from typing_extensions import Self  # type: ignore[import]
from uuid import UUID
from warnings import warn

try:
    from types import UnionType
except ImportError:
    UnionType = NotImplemented  # type: ignore
try:
    from enum import StrEnum
except ImportError:
    StrEnum = NotImplemented  # type: ignore

from pydantic import (
    BaseModel,
    AnyUrl,
    EmailStr,
    Base64Str,
    Base64Bytes,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    PrivateAttr,
    SecretStr,
    SecretBytes,
    PaymentCardNumber,
    ByteSize,
    PastDate,
    FutureDate,
    AwareDatetime,
    NaiveDatetime,
    PastDatetime,
    FutureDatetime,
    NameEmail,
    SkipValidation,
)
from pydantic.json_schema import SkipJsonSchema
from pydantic._internal._model_construction import ModelMetaclass
from pydantic_core import Url

from elasticsearch_pydantic._compat import (
    Document,
    Keyword,
    Date,
    InnerDoc,
    Object,
    Index,
    Integer,
    Nested,
    Long,
    Boolean,
    Mapping,
    Field,
    Ip,
    Double,
    Text,
    IndexMeta,
    DocumentOptions,
    DocumentMeta,
    HitMeta,
    META_FIELDS,
    DOC_META_FIELDS,
    ObjectApiResponse,
    Binary,
)


_standard_field_types: dict[Any, Callable[[], Field]] = {
    # Python types
    bool: Boolean,
    bytes: Text,
    date: Date,
    datetime: Date,
    Decimal: Double,  # Note: This may lose precision.
    Enum: Keyword,
    float: Double,  # Note: Using the widest float type to avoid precision loss.
    int: Long,  # Note: Using the widest integer type to avoid overflow.
    IntEnum: Integer,
    IPv4Address: Ip,
    IPv6Address: Ip,
    IPv4Interface: Ip,
    IPv6Interface: Ip,
    IPv4Network: Ip,
    IPv6Network: Ip,
    Path: Keyword,
    Pattern: Keyword,
    str: Text,
    StrEnum: Keyword,
    UUID: Keyword,
    # Pydantic types
    AnyUrl: Keyword,
    AwareDatetime: Date,
    Base64Bytes: Binary,
    Base64Str: Binary,
    ByteSize: Long,
    EmailStr: Keyword,
    FutureDate: Date,
    FutureDatetime: Date,
    IPvAnyAddress: Ip,
    IPvAnyInterface: Ip,
    IPvAnyNetwork: Ip,
    NaiveDatetime: Date,
    NameEmail: Keyword,
    PastDate: Date,
    PastDatetime: Date,
    PaymentCardNumber: Keyword,
    SecretBytes: Keyword,
    SecretStr: Keyword,
    Url: Keyword,
}
_standard_field_types = {
    type: field
    for type, field in _standard_field_types.items()
    if type is not NotImplemented
}


def _get_type_hint_field(
    annotation: Any,
    metadata: Sequence[Any] = tuple(),
) -> Optional[Field]:
    # Map back `Annotated` types.
    if len(metadata) > 0:
        return _get_type_hint_field(Annotated[annotation, *metadata])

    # Check if any standard type matches directly.
    for standard_type, field_type_factory in _standard_field_types.items():
        if annotation is standard_type:
            return field_type_factory()

    # Wrap `InnerDoc`s as Object field type.
    if isinstance(annotation, type) and issubclass(annotation, InnerDoc):
        return Object(annotation)

    # For the remaining cases, we need to inspect the type origin and arguments.
    origin = get_origin(annotation)
    args: Sequence[Any] = get_args(annotation)

    # Handle `Literals` as keywords.
    if origin is Literal:
        return Keyword()

    # Handle `Optional` type by unwrapping it.
    if origin is Optional:
        if len(args) != 1:
            raise ValueError(
                f"Expected a single argument for Optional, got {len(args)}."
            )
        return _get_type_hint_field(args[0])

    # Handle `Union` type by common `Field` (if unanimous).
    if origin is Union or origin is UnionType:
        # Remove `None`'s from the `Union`.
        # args = [arg for arg in args if arg is not type(None)]

        # Get the field metadata for each argument.
        maybe_fields = [_get_type_hint_field(arg) for arg in args if arg is not None]

        # Remove empty field metadata.
        fields = [field for field in maybe_fields if field is not None]

        if len(fields) <= 0:
            return None
        elif len(fields) == 1:
            return fields[0]
        else:
            first_field = fields[0]
            if any(field != first_field for field in fields[1:]):
                raise ValueError(
                    f"Union fields must be of the same type. Found: {fields}"
                )
            return first_field

    # Handle `Annotated` type by the latest `Field` annotation (or infer from annotated type).
    if origin is Annotated:
        if len(args) < 2:
            raise ValueError(
                f"Expected at least two arguments for Annotated, got {len(args)}."
            )

        # Search for the last `Field` argument.
        for arg in reversed(args[1:]):
            if arg is None:
                continue
            if isinstance(arg, Field):
                return arg
            if isinstance(arg, type) and issubclass(arg, Field):
                return arg()

        # Otherwise, unwrap the first argument.
        return _get_type_hint_field(args[0])

    # TODO: Should we handle `Sequence[float]` as `DenseVector`?
    # TODO: Should we handle `Mapping[str, float]` as `SparseVector` or `RankFeatures`?

    # Handle `Tuple` type as `Nested` if all arguments are the same `InnerDoc` (if unanimous).
    if origin is Tuple or origin is tuple:
        args_no_ellipsis = [arg for arg in args if arg is not Ellipsis]
        if not all(
            isinstance(arg, type) and issubclass(arg, InnerDoc)
            for arg in args_no_ellipsis
        ):
            return None
        elif len(args_no_ellipsis) <= 0:
            return None
        elif len(args_no_ellipsis) == 1:
            return Nested(args_no_ellipsis[0])
        else:
            first_field = args_no_ellipsis[0]
            if any(arg is not first_field for arg in args_no_ellipsis[1:]):
                raise ValueError(
                    f"Tuple arguments must be of the same type. Found: {args_no_ellipsis}"
                )
            return Nested(first_field)

    # Wrap iterable types (e.g., lists, sets, iterators) as `Nested` if the argument is an `InnerDoc`.
    if (
        isinstance(origin, type)
        and hasattr(origin, "__iter__")
        and len(args) == 1
        and isinstance(args[0], type)
        and issubclass(args[0], InnerDoc)
    ):
        return Nested(args[0])

    # Check if any superclass matches the standard types.
    if isinstance(annotation, type):
        for base in annotation.__mro__[1:]:
            for standard_type, field_type_factory in _standard_field_types.items():
                if base is standard_type:
                    return field_type_factory()

    return None


class _ModelDocumentMeta(ModelMetaclass, DocumentMeta):
    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: Any,
    ) -> type:
        # Build document options and mapping.
        doc_options = DocumentOptions(name, bases, namespace)
        mapping: Mapping = doc_options.mapping

        # Register mapping fields based on `Field` defaults (i.e., to be backwards-compatible with elasticsearch-dsl).
        for key, value in namespace.items():
            if isinstance(value, Field):
                mapping.field(key, value)

        # Create new document class.
        new_cls: type[BaseInnerDocument] = super().__new__(
            mcs=cls,
            cls_name=name,
            bases=bases,
            namespace=namespace,
            **kwds,
        )

        # Register mappings based on type hints.
        for key, field_info in new_cls.model_fields.items():
            field = _get_type_hint_field(field_info.annotation, field_info.metadata)
            if field is not None:
                mapping.field(key, field)

        # Warn about missing Elasticsearch field types.
        for key, field_info in new_cls.model_fields.items():
            if mapping.resolve_field(key) is None:
                mro = cls.mro(cls)  # type: ignore
                warn(
                    message=f"Field '{key}' of class '{name}' has no Elasticsearch field type configured.",
                    stacklevel=2 + mro.index(_ModelDocumentMeta),
                )

        # Assign document type to the new class.
        new_cls._doc_type = doc_options

        return new_cls


class _ModelIndexMeta(_ModelDocumentMeta, IndexMeta):
    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: Any,
    ) -> type:
        # Strip internal attributes from namespace and annotations.
        annotations = namespace.get("__annotations__", {})
        namespace.pop("_index", None)
        annotations.pop("_index", None)

        # Create new document class.
        new_cls: type[BaseDocument] = super().__new__(
            cls, name, bases, namespace, **kwds
        )  # type: ignore

        # Associate index with document class (but not the base class).
        if len(bases) > 2:
            index_opts = namespace.pop("Index", None)
            index: Index = cls.construct_index(index_opts, bases)
            new_cls._index = index
            index.document(new_cls)

        return new_cls


class BaseInnerDocument(
    BaseModel,
    InnerDoc,
    metaclass=_ModelDocumentMeta,
    validate_assignment=True,
    arbitrary_types_allowed=True,
):
    _meta: Annotated[HitMeta, PrivateAttr(), SkipValidation, SkipJsonSchema]
    _doc_type: Annotated[DocumentOptions, PrivateAttr(), SkipValidation, SkipJsonSchema]

    def __init__(
        self,
        /,
        meta: dict[str, Any] | None = None,
        **data: Any,
    ) -> None:
        if meta is None:
            meta = {}

        # Extract meta fields from data.
        for key in data.keys():
            if key.startswith("_") and key[1:] in META_FIELDS:
                meta[key] = data.pop(key)

        # Initialize the document.
        super().__init__(**data)

        # Update meta information.
        self._meta = HitMeta(meta)

    @property
    def meta(self) -> HitMeta:  # type: ignore[override]
        if self._meta is None:
            raise RuntimeError("Meta information is not set.")
        return self._meta

    @classmethod
    def from_es(cls, data: dict[str, Any], data_only: bool = False) -> Self:  # type: ignore[override]
        if data_only:
            data = {"_source": data}
        meta = data.copy()
        return cls(
            meta=meta,
            **meta.pop("_source", {}),
        )

    def to_dict(self, skip_empty: bool = True) -> dict[str, Any]:
        return self.model_dump(
            mode="json",
            exclude_unset=skip_empty,
        )

    # Explicitly override methods with Pydantic super calls.

    def __getstate__(self) -> dict[Any, Any]:  # type: ignore[override]
        return super().__getstate__()

    def __setstate__(self, state: dict[Any, Any]) -> None:  # type: ignore[override]
        super().__setstate__(state)

    def __iter__(self) -> Iterator[tuple[str, Any]]:  # type: ignore[override]
        return super().__iter__()


class BaseDocument(
    BaseModel,
    Document,
    metaclass=_ModelIndexMeta,
    validate_assignment=True,
    arbitrary_types_allowed=True,
):
    _meta: Annotated[HitMeta, PrivateAttr(), SkipValidation, SkipJsonSchema]
    _index: Annotated[Index, PrivateAttr(), SkipValidation, SkipJsonSchema]
    _doc_type: Annotated[DocumentOptions, PrivateAttr(), SkipValidation, SkipJsonSchema]

    def __init__(
        self,
        /,
        id: str | None = None,
        meta: dict[str, Any] | None = None,
        **data: Any,
    ) -> None:
        if meta is None:
            meta = {}

        # Extract meta fields from data.
        for key in data.keys():
            if key.startswith("_") and key[1:] in META_FIELDS:
                meta[key] = data.pop(key)

        # Initialize the document.
        super().__init__(**data)

        # Set document ID.
        if id is not None:
            meta["_id"] = id

        # Update meta information.
        self._meta = HitMeta(meta)

    @property
    def meta(self) -> HitMeta:  # type: ignore[override]
        if self._meta is None:
            raise RuntimeError("Meta information is not set.")
        return self._meta

    @classmethod
    def from_es(cls, hit: Union[dict[str, Any], ObjectApiResponse[Any]]) -> Self:
        super().from_es(hit)
        meta = hit.copy()
        return cls(
            meta=meta,
            id=meta.pop("_id", None),
            **meta.pop("_source", {}),
        )

    def to_dict(  # type: ignore[override]
        self,
        include_meta: bool = False,
        skip_empty: bool = True,
    ) -> dict[str, Any]:
        doc = self.model_dump(
            mode="json",
            exclude_unset=skip_empty,
        )
        if not include_meta:
            return doc

        meta = {
            f"_{key}": self.meta[key] for key in DOC_META_FIELDS if key in self.meta
        }

        index = self._get_index(required=False)
        if index is not None:
            meta["_index"] = index

        meta["_source"] = doc

        return meta

    def create_action(self) -> dict:
        return self.to_dict(include_meta=True)

    def update_action(
        self,
        retry_on_conflict: int | None = 3,
        **fields,
    ) -> dict:
        updated = self.model_copy(update=fields)
        doc = updated.model_dump(
            mode="json",
            include={key for key, _ in fields.items()},
            exclude={"meta"},
            exclude_unset=True,
        )

        action = {
            f"_{key}": self.meta[key]
            for key in META_FIELDS.difference({"score"})
            if key in self.meta
        }
        action["_op_type"] = "update"
        if retry_on_conflict is not None:
            action["_retry_on_conflict"] = retry_on_conflict
        action["doc"] = doc
        return action

    def delete_action(self) -> dict:
        action = {
            f"_{key}": self.meta[key]
            for key in META_FIELDS.difference({"score", "_source"})
            if key in self.meta
        }
        action["_op_type"] = "delete"
        return action

    @property
    def id(self) -> UUID:
        return UUID(self.meta.id)

    @id.setter
    def id(self, value: UUID) -> None:
        self.meta.id = str(value)

    # Explicitly override methods with Pydantic super calls.

    def __getstate__(self) -> dict[Any, Any]:  # type: ignore[override]
        return super().__getstate__()

    def __setstate__(self, state: dict[Any, Any]) -> None:  # type: ignore[override]
        super().__setstate__(state)

    def __iter__(self) -> Iterator[tuple[str, Any]]:  # type: ignore[override]
        return super().__iter__()
