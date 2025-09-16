from collections import deque
from datetime import datetime, date
from decimal import Decimal
from enum import Enum, IntEnum, StrEnum
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
    Any,
    Pattern,
    Union,
    Optional,
    Annotated,
    Sequence,
    Set,
    List,
    Tuple,
    Iterable,
    Deque,
    FrozenSet,
    AbstractSet,
)
from uuid import UUID

from pydantic import (
    AnyUrl,
    EmailStr,
    Base64Str,
    Base64Bytes,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
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
)
from pydantic_core import Url
from typing_extensions import TypeAlias  # type: ignore[import]

from elasticsearch_pydantic import BaseDocument, BaseInnerDocument
from elasticsearch_pydantic.field import (
    BinaryField,
    BooleanField,
    ByteField,
    CompletionField,
    ConstantKeywordField,  # type: ignore[no-redef]
    DateField,
    DatetimeField,
    DateRangeField,
    DatetimeRangeField,
    DoubleField,
    DoubleRangeField,
    FloatField,
    FloatRangeField,
    HalfFloatField,
    IntegerField,
    IntegerRangeField,
    IpField,
    IpRangeField,
    KeywordField,
    LongField,
    LongRangeField,
    RankFeatureField,  # type: ignore[no-redef]
    SearchAsYouTypeField,  # type: ignore[no-redef]
    ShortField,
    SparseVectorField,  # type: ignore[no-redef]
    TextField,
    TokenCountField,
)
from elasticsearch_pydantic._compat import (
    Field,
    Document,
    InnerDoc,
    Binary,
    Boolean,
    Byte,
    Completion,
    ConstantKeyword,
    Date,
    DateRange,
    Double,
    DoubleRange,
    Float,
    FloatRange,
    HalfFloat,
    Integer,
    IntegerRange,
    Ip,
    IpRange,
    Keyword,
    Long,
    LongRange,
    RankFeature,
    RankFeatures,
    SearchAsYouType,
    Short,
    SparseVector,
    Text,
    TokenCount,
    Object,
    Nested,
    Mapping,
)

# Re-define missing types as `Field` to avoid `NotImplemented` checks everywhere.
if ConstantKeyword is NotImplemented:
    ConstantKeyword: TypeAlias = Field  # type: ignore[no-redef]
    ConstantKeywordField: TypeAlias = Annotated[Any, Field]  # type: ignore[no-redef,misc]
if RankFeature is NotImplemented:
    RankFeature: TypeAlias = Field  # type: ignore[no-redef]
    RankFeatureField: TypeAlias = Annotated[Any, Field]  # type: ignore[no-redef,misc]
if RankFeatures is NotImplemented:
    RankFeatures: TypeAlias = Field  # type: ignore[no-redef]
    RankFeaturesField: TypeAlias = Annotated[Any, Field]  # type: ignore[no-redef,misc]
if SearchAsYouType is NotImplemented:
    SearchAsYouType: TypeAlias = Field  # type: ignore[no-redef]
    SearchAsYouTypeField: TypeAlias = Annotated[Any, Field]  # type: ignore[no-redef,misc]
if SparseVector is NotImplemented:
    SparseVector: TypeAlias = Field  # type: ignore[no-redef]
    SparseVectorField: TypeAlias = Annotated[Any, Field]  # type: ignore[no-redef,misc]


def _assert_mapping_equal(doc1: type[Document], doc2: type[Document]) -> None:
    """
    Assert that the mappings of two `Document` classes are equal.
    This includes checking that each field has the same type and `required` and `multi` settings.
    """
    assert doc1._doc_type.mapping.to_dict() == doc2._doc_type.mapping.to_dict()
    properties1 = doc1._doc_type.mapping.properties.properties
    properties2 = doc2._doc_type.mapping.properties.properties
    assert dir(properties1) == dir(properties2)
    for key in dir(properties1):
        property1: Field = properties1[key]
        property2: Field = properties2[key]
        assert property1 == property2
        assert property1._required == property2._required, (
            f"{property1}._required != {property2}._required in field {key} of {doc1} and {doc2}"
        )
        assert property1._multi == property2._multi, (
            f"{property1}._multi != {property2}._multi in field {key} of {doc1} and {doc2}"
        )


def test_mapping_standard_type_annotation() -> Any:
    class _OldDocument(Document):
        # Python types
        bool_field = Boolean(required=True, multi=False)
        bytes_field = Text(required=True, multi=False)
        date_field = Date(required=True, multi=False)
        datetime_field = Date(required=True, multi=False)
        decimal_field = Double(required=True, multi=False)
        enum_field = Keyword(required=True, multi=False)
        float_field = Double(required=True, multi=False)
        int_field = Long(required=True, multi=False)
        int_enum_field = Integer(required=True, multi=False)
        ipv4_address_field = Ip(required=True, multi=False)
        ipv6_address_field = Ip(required=True, multi=False)
        ipv4_interface_field = Ip(required=True, multi=False)
        ipv6_interface_field = Ip(required=True, multi=False)
        ipv4_network_field = Ip(required=True, multi=False)
        ipv6_network_field = Ip(required=True, multi=False)
        path_field = Keyword(required=True, multi=False)
        pattern_field = Keyword(required=True, multi=False)
        str_field = Text(required=True, multi=False)
        str_enum_field = Keyword(required=True, multi=False)
        uuid_field = Keyword(required=True, multi=False)
        # Pydantic types
        any_url_field = Keyword(required=True, multi=False)
        aware_datetime_field = Date(required=True, multi=False)
        base64_bytes_field = Binary(required=True, multi=False)
        base64_str_field = Binary(required=True, multi=False)
        byte_size_field = Long(required=True, multi=False)
        email_str_field = Keyword(required=True, multi=False)
        future_date_field = Date(required=True, multi=False)
        future_datetime_field = Date(required=True, multi=False)
        ipv_any_address_field = Ip(required=True, multi=False)
        ipv_any_interface_field = Ip(required=True, multi=False)
        ipv_any_network_field = Ip(required=True, multi=False)
        naive_datetime_field = Date(required=True, multi=False)
        name_email_field = Keyword(required=True, multi=False)
        past_date_field = Date(required=True, multi=False)
        past_datetime_field = Date(required=True, multi=False)
        payment_card_number_field = Keyword(required=True, multi=False)
        secret_bytes_field = Keyword(required=True, multi=False)
        secret_str_field = Keyword(required=True, multi=False)
        url_field = Keyword(required=True, multi=False)

        class Index:
            pass

    class _Enum(Enum):
        A = "A"
        B = "B"

    class _IntEnum(IntEnum):
        A = 1
        B = 2

    class _StrEnum(StrEnum):
        A = "A"
        B = "B"

    class _NewDocument(BaseDocument):
        # Python types
        bool_field: bool
        bytes_field: bytes
        date_field: date
        datetime_field: datetime
        decimal_field: Decimal
        enum_field: _Enum
        float_field: float
        int_field: int
        int_enum_field: _IntEnum
        ipv4_address_field: IPv4Address
        ipv6_address_field: IPv6Address
        ipv4_interface_field: IPv4Interface
        ipv6_interface_field: IPv6Interface
        ipv4_network_field: IPv4Network
        ipv6_network_field: IPv6Network
        path_field: Path
        pattern_field: Pattern
        str_field: str
        str_enum_field: _StrEnum
        uuid_field: UUID
        # Pydantic types
        any_url_field: AnyUrl
        aware_datetime_field: AwareDatetime
        base64_bytes_field: Base64Bytes
        base64_str_field: Base64Str
        byte_size_field: ByteSize
        email_str_field: EmailStr
        future_date_field: FutureDate
        future_datetime_field: FutureDatetime
        ipv_any_address_field: IPvAnyAddress
        ipv_any_interface_field: IPvAnyInterface
        ipv_any_network_field: IPvAnyNetwork
        naive_datetime_field: NaiveDatetime
        name_email_field: NameEmail
        past_date_field: PastDate
        past_datetime_field: PastDatetime
        payment_card_number_field: PaymentCardNumber
        secret_bytes_field: SecretBytes
        secret_str_field: SecretStr
        url_field: Url

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)


def test_mapping_standard_type_annotation_multi() -> Any:
    class _OldDocument(Document):
        # Python types
        bool_field = Boolean(required=True, multi=True)
        bytes_field = Text(required=True, multi=True)
        date_field = Date(required=True, multi=True)
        datetime_field = Date(required=True, multi=True)
        decimal_field = Double(required=True, multi=True)
        enum_field = Keyword(required=True, multi=True)
        float_field = Double(required=True, multi=True)
        int_field = Long(required=True, multi=True)
        int_enum_field = Integer(required=True, multi=True)
        ipv4_address_field = Ip(required=True, multi=True)
        ipv6_address_field = Ip(required=True, multi=True)
        ipv4_interface_field = Ip(required=True, multi=True)
        ipv6_interface_field = Ip(required=True, multi=True)
        ipv4_network_field = Ip(required=True, multi=True)
        ipv6_network_field = Ip(required=True, multi=True)
        path_field = Keyword(required=True, multi=True)
        pattern_field = Keyword(required=True, multi=True)
        str_field = Text(required=True, multi=True)
        str_enum_field = Keyword(required=True, multi=True)
        uuid_field = Keyword(required=True, multi=True)
        # Pydantic types
        any_url_field = Keyword(required=True, multi=True)
        aware_datetime_field = Date(required=True, multi=True)
        base64_bytes_field = Binary(required=True, multi=True)
        base64_str_field = Binary(required=True, multi=True)
        byte_size_field = Long(required=True, multi=True)
        email_str_field = Keyword(required=True, multi=True)
        future_date_field = Date(required=True, multi=True)
        future_datetime_field = Date(required=True, multi=True)
        ipv_any_address_field = Ip(required=True, multi=True)
        ipv_any_interface_field = Ip(required=True, multi=True)
        ipv_any_network_field = Ip(required=True, multi=True)
        naive_datetime_field = Date(required=True, multi=True)
        name_email_field = Keyword(required=True, multi=True)
        past_date_field = Date(required=True, multi=True)
        past_datetime_field = Date(required=True, multi=True)
        payment_card_number_field = Keyword(required=True, multi=True)
        secret_bytes_field = Keyword(required=True, multi=True)
        secret_str_field = Keyword(required=True, multi=True)
        url_field = Keyword(required=True, multi=True)

        class Index:
            pass

    class _Enum(Enum):
        A = "A"
        B = "B"

    class _IntEnum(IntEnum):
        A = 1
        B = 2

    class _StrEnum(StrEnum):
        A = "A"
        B = "B"

    class _NewDocument(BaseDocument):
        # Python types
        bool_field: Iterable[bool]
        bytes_field: Iterable[bytes]
        date_field: Iterable[date]
        datetime_field: Iterable[datetime]
        decimal_field: Iterable[Decimal]
        enum_field: Iterable[_Enum]
        float_field: Iterable[float]
        int_field: Iterable[int]
        int_enum_field: Iterable[_IntEnum]
        ipv4_address_field: Iterable[IPv4Address]
        ipv6_address_field: Iterable[IPv6Address]
        ipv4_interface_field: Iterable[IPv4Interface]
        ipv6_interface_field: Iterable[IPv6Interface]
        ipv4_network_field: Iterable[IPv4Network]
        ipv6_network_field: Iterable[IPv6Network]
        path_field: Iterable[Path]
        pattern_field: Iterable[Pattern]
        str_field: Iterable[str]
        str_enum_field: Iterable[_StrEnum]
        uuid_field: Iterable[UUID]
        # Pydantic types
        any_url_field: Iterable[AnyUrl]
        aware_datetime_field: Iterable[AwareDatetime]
        base64_bytes_field: Iterable[Base64Bytes]
        base64_str_field: Iterable[Base64Str]
        byte_size_field: Iterable[ByteSize]
        email_str_field: Iterable[EmailStr]
        future_date_field: Iterable[FutureDate]
        future_datetime_field: Iterable[FutureDatetime]
        ipv_any_address_field: Iterable[IPvAnyAddress]
        ipv_any_interface_field: Iterable[IPvAnyInterface]
        ipv_any_network_field: Iterable[IPvAnyNetwork]
        naive_datetime_field: Iterable[NaiveDatetime]
        name_email_field: Iterable[NameEmail]
        past_date_field: Iterable[PastDate]
        past_datetime_field: Iterable[PastDatetime]
        payment_card_number_field: Iterable[PaymentCardNumber]
        secret_bytes_field: Iterable[SecretBytes]
        secret_str_field: Iterable[SecretStr]
        url_field: Iterable[Url]

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)


def test_mapping_field_type_annotation() -> Any:
    class _OldDocument(Document):
        binary_field = Binary(required=True, multi=False)
        boolean_field = Boolean(required=True, multi=False)
        byte_field = Byte(required=True, multi=False)
        completion_field = Completion(required=True, multi=False)
        constant_keyword_field = ConstantKeyword(required=True, multi=False)
        date_field = Date(required=True, multi=False)
        datetime_field = Date(required=True, multi=False)
        date_range_field = DateRange(required=True, multi=False)
        datetime_range_field = DateRange(required=True, multi=False)
        double_field = Double(required=True, multi=False)
        double_range_field = DoubleRange(required=True, multi=False)
        float_field = Float(required=True, multi=False)
        float_range_field = FloatRange(required=True, multi=False)
        half_float_field = HalfFloat(required=True, multi=False)
        integer_field = Integer(required=True, multi=False)
        integer_range_field = IntegerRange(required=True, multi=False)
        ip_field = Ip(required=True, multi=False)
        ip_range_field = IpRange(required=True, multi=False)
        keyword_field = Keyword(required=True, multi=False)
        long_field = Long(required=True, multi=False)
        long_range_field = LongRange(required=True, multi=False)
        rank_feature_field = RankFeature(required=True, multi=False)
        rank_features_field = RankFeatures(required=True, multi=False)
        search_as_you_type_field = SearchAsYouType(required=True, multi=False)
        short_field = Short(required=True, multi=False)
        sparse_vector_field = SparseVector(required=True, multi=False)
        text_field = Text(required=True, multi=False)
        token_count_field = TokenCount(required=True, multi=False)

        class Index:
            pass

    class _NewDocument(BaseDocument):
        binary_field: BinaryField
        boolean_field: BooleanField
        byte_field: ByteField
        completion_field: CompletionField
        constant_keyword_field: ConstantKeywordField
        date_field: DateField
        datetime_field: DatetimeField
        date_range_field: DateRangeField
        datetime_range_field: DatetimeRangeField
        double_field: DoubleField
        double_range_field: DoubleRangeField
        float_field: FloatField
        float_range_field: FloatRangeField
        half_float_field: HalfFloatField
        integer_field: IntegerField
        integer_range_field: IntegerRangeField
        ip_field: IpField
        ip_range_field: IpRangeField
        keyword_field: KeywordField
        long_field: LongField
        long_range_field: LongRangeField
        rank_feature_field: RankFeatureField
        rank_features_field: RankFeaturesField
        search_as_you_type_field: SearchAsYouTypeField
        short_field: ShortField
        sparse_vector_field: SparseVectorField
        text_field: TextField
        token_count_field: TokenCountField

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)


def test_mapping_field_type_annotation_multi() -> Any:
    class _OldDocument(Document):
        binary_field = Binary(required=True, multi=True)
        boolean_field = Boolean(required=True, multi=True)
        byte_field = Byte(required=True, multi=True)
        completion_field = Completion(required=True, multi=True)
        # constant_keyword_field = ConstantKeyword(required=True, multi=True)
        date_field = Date(required=True, multi=True)
        datetime_field = Date(required=True, multi=True)
        date_range_field = DateRange(required=True, multi=True)
        datetime_range_field = DateRange(required=True, multi=True)
        double_field = Double(required=True, multi=True)
        double_range_field = DoubleRange(required=True, multi=True)
        float_field = Float(required=True, multi=True)
        float_range_field = FloatRange(required=True, multi=True)
        half_float_field = HalfFloat(required=True, multi=True)
        integer_field = Integer(required=True, multi=True)
        integer_range_field = IntegerRange(required=True, multi=True)
        ip_field = Ip(required=True, multi=True)
        ip_range_field = IpRange(required=True, multi=True)
        keyword_field = Keyword(required=True, multi=True)
        long_field = Long(required=True, multi=True)
        long_range_field = LongRange(required=True, multi=True)
        # rank_feature_field = RankFeature(required=True, multi=True)
        # rank_features_field = RankFeatures(required=True, multi=True)
        # search_as_you_type_field = SearchAsYouType(required=True, multi=True)
        short_field = Short(required=True, multi=True)
        # sparse_vector_field = SparseVector(required=True, multi=True)
        text_field = Text(required=True, multi=True)
        token_count_field = TokenCount(required=True, multi=True)

        class Index:
            pass

    class _NewDocument(BaseDocument):
        binary_field: Iterable[BinaryField]
        boolean_field: Iterable[BooleanField]
        byte_field: Iterable[ByteField]
        completion_field: Iterable[CompletionField]
        # constant_keyword_field: Iterable[ConstantKeywordField]
        date_field: Iterable[DateField]
        datetime_field: Iterable[DatetimeField]
        date_range_field: Iterable[DateRangeField]
        datetime_range_field: Iterable[DatetimeRangeField]
        double_field: Iterable[DoubleField]
        double_range_field: Iterable[DoubleRangeField]
        float_field: Iterable[FloatField]
        float_range_field: Iterable[FloatRangeField]
        half_float_field: Iterable[HalfFloatField]
        integer_field: Iterable[IntegerField]
        integer_range_field: Iterable[IntegerRangeField]
        ip_field: Iterable[IpField]
        ip_range_field: Iterable[IpRangeField]
        keyword_field: Iterable[KeywordField]
        long_field: Iterable[LongField]
        long_range_field: Iterable[LongRangeField]
        # rank_feature_field: Iterable[RankFeatureField]
        # rank_features_field: Iterable[RankFeaturesField]
        # search_as_you_type_field: Iterable[SearchAsYouTypeField]
        short_field: Iterable[ShortField]
        # sparse_vector_field: Iterable[SparseVectorField]
        text_field: Iterable[TextField]
        token_count_field: Iterable[TokenCountField]

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)


def test_mapping_with_object() -> Any:
    class _OldInner(InnerDoc):
        int_field = Integer(required=True, multi=False)

    class _OldDocument(Document):
        object_field = Object(_OldInner, required=True, multi=False)

        class Index:
            pass

    class _NewInner(BaseInnerDocument):
        int_field: IntegerField

    class _NewDocument(BaseDocument):
        object_field: _NewInner

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)


def test_mapping_with_nested() -> Any:
    class _OldInner(InnerDoc):
        int_field = Integer(required=True, multi=False)

    class _OldDocument(Document):
        nested_list_field = Nested(_OldInner, required=True, multi=True)
        nested_typing_list_field = Nested(_OldInner, required=True, multi=True)
        nested_set_field = Nested(_OldInner, required=True, multi=True)
        nested_typing_set_field = Nested(_OldInner, required=True, multi=True)
        nested_abstract_set_field = Nested(_OldInner, required=True, multi=True)
        nested_frozenset_field = Nested(_OldInner, required=True, multi=True)
        nested_typing_frozenset_field = Nested(_OldInner, required=True, multi=True)
        nested_tuple_field = Nested(_OldInner, required=True, multi=True)
        nested_typing_tuple_field = Nested(_OldInner, required=True, multi=True)
        nested_tuple_ellipsis_field = Nested(_OldInner, required=True, multi=True)
        nested_typing_tuple_ellipsis_field = Nested(
            _OldInner, required=True, multi=True
        )
        nested_sequence_field = Nested(_OldInner, required=True, multi=True)
        nested_deque_field = Nested(_OldInner, required=True, multi=True)
        nested_typing_deque_field = Nested(_OldInner, required=True, multi=True)
        nested_iterable_field = Nested(_OldInner, required=True, multi=True)

        class Index:
            pass

    class _NewInner(BaseInnerDocument):
        int_field: IntegerField

    class _NewDocument(BaseDocument):
        nested_list_field: list[_NewInner]
        nested_typing_list_field: List[_NewInner]
        nested_set_field: set[_NewInner]
        nested_typing_set_field: Set[_NewInner]
        nested_abstract_set_field: AbstractSet[_NewInner]
        nested_frozenset_field: frozenset[_NewInner]
        nested_typing_frozenset_field: FrozenSet[_NewInner]
        nested_tuple_field: tuple[_NewInner, _NewInner]
        nested_typing_tuple_field: Tuple[_NewInner, _NewInner]
        nested_tuple_ellipsis_field: tuple[_NewInner, ...]
        nested_typing_tuple_ellipsis_field: Tuple[_NewInner, ...]
        nested_sequence_field: Sequence[_NewInner]
        nested_deque_field: deque[_NewInner]
        nested_typing_deque_field: Deque[_NewInner]
        nested_iterable_field: Iterable[_NewInner]

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)


def test_mapping_with_optional() -> Any:
    class _OldDocument(Document):
        optional_standard_type_annotation = Boolean(required=False, multi=False)
        optional_operator_standard_type_annotation = Boolean(
            required=False, multi=False
        )
        optional_field_type_annotation = Boolean(required=False, multi=False)
        optional_operator_field_type_annotation = Boolean(required=False, multi=False)
        optional_standard_type_annotation_multi = Boolean(required=False, multi=True)
        optional_operator_standard_type_annotation_multi = Boolean(
            required=False, multi=True
        )
        optional_field_type_annotation_multi = Boolean(required=False, multi=True)
        optional_operator_field_type_annotation_multi = Boolean(
            required=False, multi=True
        )

        class Index:
            pass

    class _NewDocument(BaseDocument):
        optional_standard_type_annotation: Optional[bool]
        optional_operator_standard_type_annotation: bool | None
        optional_field_type_annotation: Optional[BooleanField]
        optional_operator_field_type_annotation: BooleanField | None
        optional_standard_type_annotation_multi: Optional[List[bool]]
        optional_operator_standard_type_annotation_multi: List[bool] | None
        optional_field_type_annotation_multi: Optional[List[BooleanField]]
        optional_operator_field_type_annotation_multi: List[BooleanField] | None

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)


def test_mapping_with_union() -> Any:
    class _OldDocument(Document):
        union_field = Boolean(required=True, multi=False)
        union_operator_field = Boolean(required=True, multi=False)
        union_field_multi = Boolean(required=True, multi=True)
        union_operator_field_multi = Boolean(required=True, multi=True)

        class Index:
            pass

    class _NewDocument(BaseDocument):
        union_field: Union[bool, Annotated[int, Boolean], Annotated[float, Boolean]]
        union_operator_field: bool | Annotated[int, Boolean] | Annotated[float, Boolean]
        union_field_multi: Iterable[
            Union[bool, Annotated[int, Boolean], Annotated[float, Boolean]]
        ]
        union_operator_field_multi: Iterable[
            bool | Annotated[int, Boolean] | Annotated[float, Boolean]
        ]

        class Index:
            pass

    actual = _NewDocument
    expected = _OldDocument
    _assert_mapping_equal(actual, expected)
