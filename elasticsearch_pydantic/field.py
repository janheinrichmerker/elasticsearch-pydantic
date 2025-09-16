from datetime import datetime, date
from typing import Annotated, Generic, TypeVar, Mapping
from typing_extensions import TypeAlias  # type: ignore[import]

from annotated_types import Interval
from pydantic import BaseModel, Base64Str, IPvAnyAddress

from elasticsearch_pydantic._compat import (
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
)

_T = TypeVar("_T")


class Range(BaseModel, Generic[_T]):
    gt: _T | None = None
    gte: _T | None = None
    lt: _T | None = None
    lte: _T | None = None


BinaryField: TypeAlias = Annotated[Base64Str, Binary]
BooleanField: TypeAlias = Annotated[bool, Boolean]
ByteField: TypeAlias = Annotated[int, Interval(ge=-128, le=127), Byte]
CompletionField: TypeAlias = Annotated[str, Completion]
if ConstantKeyword is not NotImplemented:
    ConstantKeywordField: TypeAlias = Annotated[str, ConstantKeyword]
else:
    ConstantKeywordField = NotImplemented  # type: ignore
DateField: TypeAlias = Annotated[date, Date]
DatetimeField: TypeAlias = Annotated[datetime, Date]
DateRangeField: TypeAlias = Annotated[Range[date], DateRange]
DatetimeRangeField: TypeAlias = Annotated[Range[datetime], DateRange]
DoubleField: TypeAlias = Annotated[
    float, Double
]  # TODO: Can we constrain to double-precision 64-bit IEEE 754?
DoubleRangeField: TypeAlias = Annotated[
    Range[float], DoubleRange
]  # TODO: Can we constrain to double-precision 64-bit IEEE 754?
FloatField: TypeAlias = Annotated[
    float, Float
]  # TODO: Can we constrain to single-precision 32-bit IEEE 754?
FloatRangeField: TypeAlias = Annotated[
    Range[float], FloatRange
]  # TODO: Can we constrain to single-precision 32-bit IEEE 754?
HalfFloatField: TypeAlias = Annotated[
    float, HalfFloat
]  # TODO: Can we constrain to half-precision 16-bit IEEE 754?
IntegerField: TypeAlias = Annotated[
    int, Interval(ge=-2147483648, le=2147483647), Integer
]
IntegerRangeField: TypeAlias = Annotated[
    Range[Annotated[int, Interval(ge=-2147483648, le=2147483647)]], IntegerRange
]
IpField: TypeAlias = Annotated[IPvAnyAddress, Ip]
IpRangeField: TypeAlias = Annotated[Range[IPvAnyAddress], IpRange]
KeywordField: TypeAlias = Annotated[str, Keyword]
LongField: TypeAlias = Annotated[
    int, Interval(ge=-9223372036854775808, le=9223372036854775807), Long
]
LongRangeField: TypeAlias = Annotated[
    Range[Annotated[int, Interval(ge=-9223372036854775808, le=9223372036854775807)]],
    LongRange,
]
if RankFeature is not NotImplemented:
    RankFeatureField: TypeAlias = Annotated[float, RankFeature]
else:
    RankFeatureField = NotImplemented  # type: ignore
if RankFeatures is not NotImplemented:
    RankFeaturesField: TypeAlias = Annotated[Mapping[str, float], RankFeatures]
else:
    RankFeaturesField = NotImplemented  # type: ignore
if SearchAsYouType is not NotImplemented:
    SearchAsYouTypeField: TypeAlias = Annotated[str, SearchAsYouType]
else:
    SearchAsYouTypeField = NotImplemented  # type: ignore
ShortField: TypeAlias = Annotated[int, Interval(ge=-32768, le=32767), Short]
if SparseVector is not NotImplemented:
    SparseVectorField: TypeAlias = Annotated[Mapping[str, float], SparseVector]
else:
    SparseVectorField = NotImplemented  # type: ignore
TextField: TypeAlias = Annotated[str, Text]
TokenCountField: TypeAlias = Annotated[int, TokenCount]

# TODO: GeoPoint, GeoShape, Join, Murmur3, Percolator, Point, Shape, TokenCount
# Note: The geo-related fields could, for example, be validated using https://github.com/developmentseed/geojson-pydantic or
