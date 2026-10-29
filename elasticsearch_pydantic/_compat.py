from importlib.metadata import PackageNotFoundError, metadata, version

from elastic_transport._response import ObjectApiResponse
from packaging.version import Version

__all__ = [
    "AttrDict",
    "Binary",
    "Boolean",
    "Byte",
    "Completion",
    "Date",
    "DateRange",
    "Document",
    "DocumentMeta",
    "DocumentOptions",
    "Double",
    "DoubleRange",
    "Elasticsearch",
    "Field",
    "Float",
    "FloatRange",
    "HalfFloat",
    "HitMeta",
    "Index",
    "IndexMeta",
    "InnerDoc",
    "Integer",
    "IntegerRange",
    "Ip",
    "IpRange",
    "Keyword",
    "Long",
    "LongRange",
    "Mapping",
    "Nested",
    "Object",
    "ObjectApiResponse",
    "RankFeature",
    "RankFeatures",
    "SearchAsYouType",
    "Short",
    "SparseVector",
    "Text",
    "TokenCount",
]


def _is_installed(distribution_name: str) -> bool:
    try:
        metadata(distribution_name=distribution_name)
        return True
    except PackageNotFoundError:
        return False


def _is_version_at_least(distribution_name: str, at_least_version: str) -> bool:
    version_str = version(distribution_name=distribution_name)
    return Version(version_str) >= Version(at_least_version)


if _is_installed("elasticsearch8-dsl"):
    if _is_version_at_least("elasticsearch8-dsl", "8.12.0"):
        raise ImportError("Elasticsearch DSL version below 8.12.0 is required.")
    from elasticsearch import Elasticsearch
    from elasticsearch8_dsl import (
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Document,
        Double,
        DoubleRange,
        Field,
        Float,
        FloatRange,
        HalfFloat,
        Index,
        InnerDoc,
        Integer,
        IntegerRange,
        Ip,
        IpRange,
        Keyword,
        Long,
        LongRange,
        Mapping,
        Nested,
        Object,
        RankFeature,
        RankFeatures,
        SearchAsYouType,
        Short,
        SparseVector,
        Text,
        TokenCount,
    )
    from elasticsearch8_dsl.document import DocumentMeta, DocumentOptions, IndexMeta
    from elasticsearch8_dsl.utils import AttrDict, HitMeta
elif _is_installed("elasticsearch7-dsl"):
    from elasticsearch7 import Elasticsearch  # type: ignore[no-redef]
    from elasticsearch7_dsl import (
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Document,
        Double,
        DoubleRange,
        Field,
        Float,
        FloatRange,
        HalfFloat,
        Index,
        InnerDoc,
        Integer,
        IntegerRange,
        Ip,
        IpRange,
        Keyword,
        Long,
        LongRange,
        Mapping,
        Nested,
        Object,
        RankFeature,
        SearchAsYouType,
        Short,
        SparseVector,
        Text,
        TokenCount,
    )
    from elasticsearch7_dsl.document import DocumentMeta, DocumentOptions, IndexMeta
    from elasticsearch7_dsl.utils import AttrDict, HitMeta

    RankFeatures = NotImplemented
elif _is_installed("elasticsearch6-dsl"):
    from elasticsearch6 import Elasticsearch  # type: ignore[no-redef]
    from elasticsearch6_dsl import (
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Document,
        Double,
        DoubleRange,
        Field,
        Float,
        FloatRange,
        HalfFloat,
        Index,
        InnerDoc,
        Integer,
        IntegerRange,
        Ip,
        IpRange,
        Keyword,
        Long,
        LongRange,
        Mapping,
        Nested,
        Object,
        Short,
        Text,
        TokenCount,
    )
    from elasticsearch6_dsl.document import DocumentMeta, DocumentOptions, IndexMeta
    from elasticsearch6_dsl.utils import AttrDict, HitMeta

    RankFeature = NotImplemented
    RankFeatures = NotImplemented
    SearchAsYouType = NotImplemented
    SparseVector = NotImplemented
elif _is_installed("elasticsearch-dsl"):
    if not _is_version_at_least("elasticsearch-dsl", "6.0.0"):
        raise ImportError("Elasticsearch DSL version 6.0.0 or higher is required.")
    if _is_version_at_least("elasticsearch-dsl", "8.12.0"):
        raise ImportError("Elasticsearch DSL version below 8.12.0 is required.")
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import (
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Document,
        Double,
        DoubleRange,
        Field,
        Float,
        FloatRange,
        HalfFloat,
        Index,
        InnerDoc,
        Integer,
        IntegerRange,
        Ip,
        IpRange,
        Keyword,
        Long,
        LongRange,
        Mapping,
        Nested,
        Object,
        Short,
        Text,
        TokenCount,
    )
    from elasticsearch_dsl.document import DocumentMeta, DocumentOptions, IndexMeta
    from elasticsearch_dsl.utils import AttrDict, HitMeta

    if _is_version_at_least("elasticsearch-dsl", "8.0.0"):
        from elasticsearch_dsl import RankFeatures
    else:
        RankFeatures = NotImplemented
    if _is_version_at_least("elasticsearch-dsl", "7.0.0"):
        from elasticsearch_dsl import RankFeature, SearchAsYouType, SparseVector
    else:
        RankFeature = NotImplemented
        SearchAsYouType = NotImplemented
        SparseVector = NotImplemented
else:
    raise ImportError("Elasticsearch DSL is not installed.")
