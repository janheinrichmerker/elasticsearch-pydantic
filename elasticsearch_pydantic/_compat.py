from importlib.metadata import metadata, PackageNotFoundError, version

from packaging.version import Version

from elastic_transport._response import ObjectApiResponse

__all__ = [
    "ObjectApiResponse",
    "Elasticsearch",
    "Document",
    "InnerDoc",
    "Index",
    "Mapping",
    "Binary",
    "Boolean",
    "Byte",
    "Completion",
    "Date",
    "DateRange",
    "Double",
    "DoubleRange",
    "Field",
    "Float",
    "FloatRange",
    "HalfFloat",
    "Integer",
    "IntegerRange",
    "Ip",
    "IpRange",
    "Keyword",
    "Long",
    "LongRange",
    "Nested",
    "Object",
    "RankFeature",
    "RankFeatures",
    "SearchAsYouType",
    "Short",
    "SparseVector",
    "Text",
    "TokenCount",
    "IndexMeta",
    "DocumentOptions",
    "DocumentMeta",
    "HitMeta",
    "AttrDict",
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
    from elasticsearch8_dsl import (
        Document,
        InnerDoc,
        Index,
        Mapping,
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Double,
        DoubleRange,
        Field,
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
    from elasticsearch8_dsl.document import IndexMeta, DocumentOptions, DocumentMeta
    from elasticsearch8_dsl.utils import HitMeta, AttrDict
    from elasticsearch import Elasticsearch
elif _is_installed("elasticsearch7-dsl"):
    from elasticsearch7_dsl import (
        Document,
        InnerDoc,
        Index,
        Mapping,
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Double,
        DoubleRange,
        Field,
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
        Nested,
        Object,
        RankFeature,
        SearchAsYouType,
        Short,
        SparseVector,
        Text,
        TokenCount,
    )
    from elasticsearch7_dsl.document import IndexMeta, DocumentOptions, DocumentMeta
    from elasticsearch7_dsl.utils import HitMeta, AttrDict
    from elasticsearch7 import Elasticsearch  # type: ignore[no-redef]

    RankFeatures = NotImplemented
elif _is_installed("elasticsearch6-dsl"):
    from elasticsearch6_dsl import (
        Document,
        InnerDoc,
        Index,
        Mapping,
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Double,
        DoubleRange,
        Field,
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
        Nested,
        Object,
        Short,
        Text,
        TokenCount,
    )
    from elasticsearch6_dsl.document import IndexMeta, DocumentOptions, DocumentMeta
    from elasticsearch6_dsl.utils import HitMeta, AttrDict
    from elasticsearch6 import Elasticsearch  # type: ignore[no-redef]

    RankFeature = NotImplemented
    RankFeatures = NotImplemented
    SearchAsYouType = NotImplemented
    SparseVector = NotImplemented
elif _is_installed("elasticsearch-dsl"):
    if not _is_version_at_least("elasticsearch-dsl", "6.0.0"):
        raise ImportError("Elasticsearch DSL version 6.0.0 or higher is required.")
    if _is_version_at_least("elasticsearch-dsl", "8.12.0"):
        raise ImportError("Elasticsearch DSL version below 8.12.0 is required.")
    from elasticsearch_dsl import (
        Document,
        InnerDoc,
        Index,
        Mapping,
        Binary,
        Boolean,
        Byte,
        Completion,
        Date,
        DateRange,
        Double,
        DoubleRange,
        Field,
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
        Nested,
        Object,
        Short,
        Text,
        TokenCount,
    )
    from elasticsearch_dsl.document import IndexMeta, DocumentOptions, DocumentMeta
    from elasticsearch_dsl.utils import HitMeta, AttrDict
    from elasticsearch import Elasticsearch

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
