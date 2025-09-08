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

from elasticsearch_pydantic import BaseDocument, BaseInnerDocument
from elasticsearch_pydantic.field import (
    BinaryField,
    BooleanField,
    ByteField,
    CompletionField,
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
    RankFeatureField,
    SearchAsYouTypeField,
    ShortField,
    SparseVectorField,
    TextField,
    TokenCountField,
)
from elasticsearch_pydantic._compat import (
    Document,
    InnerDoc,
    Binary,
    Boolean,
    Byte,
    Completion,
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
    SearchAsYouType,
    Short,
    SparseVector,
    Text,
    TokenCount,
    Object,
    Nested,
)


def _get_mapping(doc_class) -> Any:
    return doc_class._index.to_dict()


def test_mapping_standard_type_annotation() -> Any:
    class _OldDocument(Document):
        # Python types
        bool_field = Boolean()
        bytes_field = Text()
        date_field = Date()
        datetime_field = Date()
        decimal_field = Double()
        enum_field = Keyword()
        float_field = Double()
        int_field = Long()
        int_enum_field = Integer()
        ipv4_address_field = Ip()
        ipv6_address_field = Ip()
        ipv4_interface_field = Ip()
        ipv6_interface_field = Ip()
        ipv4_network_field = Ip()
        ipv6_network_field = Ip()
        path_field = Keyword()
        pattern_field = Keyword()
        str_field = Text()
        str_enum_field = Keyword()
        uuid_field = Keyword()
        # Pydantic types
        any_url_field = Keyword()
        aware_datetime_field = Date()
        base64_bytes_field = Binary()
        base64_str_field = Binary()
        byte_size_field = Long()
        email_str_field = Keyword()
        future_date_field = Date()
        future_datetime_field = Date()
        ipv_any_address_field = Ip()
        ipv_any_interface_field = Ip()
        ipv_any_network_field = Ip()
        naive_datetime_field = Date()
        name_email_field = Keyword()
        past_date_field = Date()
        past_datetime_field = Date()
        payment_card_number_field = Keyword()
        secret_bytes_field = Keyword()
        secret_str_field = Keyword()
        url_field = Keyword()

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

    actual = _get_mapping(_NewDocument)
    expected = _get_mapping(_OldDocument)
    assert actual == expected


def test_mapping_field_type_annotation() -> Any:
    class _OldDocument(Document):
        binary_field = Binary()
        boolean_field = Boolean()
        byte_field = Byte()
        completion_field = Completion()
        # constant_keyword_field = ConstantKeyword()
        date_field = Date()
        datetime_field = Date()
        date_range_field = DateRange()
        datetime_range_field = DateRange()
        double_field = Double()
        double_range_field = DoubleRange()
        float_field = Float()
        float_range_field = FloatRange()
        half_float_field = HalfFloat()
        integer_field = Integer()
        integer_range_field = IntegerRange()
        ip_field = Ip()
        ip_range_field = IpRange()
        keyword_field = Keyword()
        long_field = Long()
        long_range_field = LongRange()
        rank_feature_field = RankFeature()
        # rank_features_field = RankFeatures()
        search_as_you_type_field = SearchAsYouType()
        short_field = Short()
        sparse_vector_field = SparseVector()
        text_field = Text()
        token_count_field = TokenCount()

        class Index:
            pass

    class _NewDocument(BaseDocument):
        binary_field: BinaryField
        boolean_field: BooleanField
        byte_field: ByteField
        completion_field: CompletionField
        # constant_keyword_field: ConstantKeywordField
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
        # rank_features_field: RankFeaturesField
        search_as_you_type_field: SearchAsYouTypeField
        short_field: ShortField
        sparse_vector_field: SparseVectorField
        text_field: TextField
        token_count_field: TokenCountField

        class Index:
            pass

    actual = _get_mapping(_NewDocument)
    expected = _get_mapping(_OldDocument)
    assert actual == expected


def test_mapping_with_object() -> Any:
    class _OldInner(InnerDoc):
        int_field = Integer()

    class _OldDocument(Document):
        object_field = Object(_OldInner)

        class Index:
            pass

    class _NewInner(BaseInnerDocument):
        int_field: IntegerField

    class _NewDocument(BaseDocument):
        object_field: _NewInner

        class Index:
            pass

    actual = _get_mapping(_NewDocument)
    expected = _get_mapping(_OldDocument)
    assert actual == expected


def test_mapping_with_nested() -> Any:
    class _OldInner(InnerDoc):
        int_field = Integer()

    class _OldDocument(Document):
        nested_list_field = Nested(_OldInner)
        nested_typing_list_field = Nested(_OldInner)
        nested_set_field = Nested(_OldInner)
        nested_typing_set_field = Nested(_OldInner)
        nested_abstract_set_field = Nested(_OldInner)
        nested_frozenset_field = Nested(_OldInner)
        nested_typing_frozenset_field = Nested(_OldInner)
        nested_tuple_field = Nested(_OldInner)
        nested_typing_tuple_field = Nested(_OldInner)
        nested_tuple_ellipsis_field = Nested(_OldInner)
        nested_typing_tuple_ellipsis_field = Nested(_OldInner)
        nested_sequence_field = Nested(_OldInner)
        nested_deque_field = Nested(_OldInner)
        nested_typing_deque_field = Nested(_OldInner)
        nested_iterable_field = Nested(_OldInner)

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

    actual = _get_mapping(_NewDocument)
    expected = _get_mapping(_OldDocument)
    assert actual == expected


def test_mapping_with_optional() -> Any:
    class _OldDocument(Document):
        optional_field = Boolean()
        optional_operator_field = Boolean()

        class Index:
            pass

    class _NewDocument(BaseDocument):
        optional_field: Optional[bool]
        optional_operator_field: Optional[bool]

        class Index:
            pass

    actual = _get_mapping(_NewDocument)
    expected = _get_mapping(_OldDocument)
    assert actual == expected


def test_mapping_with_union() -> Any:
    class _OldDocument(Document):
        union_field = Boolean()
        union_operator_field = Boolean()

        class Index:
            pass

    class _NewDocument(BaseDocument):
        union_field: Union[bool, Annotated[int, Boolean], Annotated[float, Boolean]]
        union_operator_field: bool | Annotated[int, Boolean] | Annotated[float, Boolean]

        class Index:
            pass

    actual = _get_mapping(_NewDocument)
    expected = _get_mapping(_OldDocument)
    assert actual == expected
