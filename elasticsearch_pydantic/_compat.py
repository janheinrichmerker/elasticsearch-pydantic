from importlib.metadata import metadata, PackageNotFoundError, version
from packaging.version import Version

from elastic_transport._response import ObjectApiResponse as ObjectApiResponse


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
    from elasticsearch8_dsl import (  # type: ignore[no-redef]
        Document as Document,
        InnerDoc as InnerDoc,
        Index as Index,
        Mapping as Mapping,
        Binary as Binary,
        Boolean as Boolean,
        Byte as Byte,
        Completion as Completion,
        Date as Date,
        DateRange as DateRange,
        Double as Double,
        DoubleRange as DoubleRange,
        Field as Field,
        Float as Float,
        FloatRange as FloatRange,
        HalfFloat as HalfFloat,
        Integer as Integer,
        IntegerRange as IntegerRange,
        Ip as Ip,
        IpRange as IpRange,
        Keyword as Keyword,
        Long as Long,
        LongRange as LongRange,
        Nested as Nested,
        Object as Object,
        RankFeature as RankFeature,
        RankFeatures as RankFeatures,
        SearchAsYouType as SearchAsYouType,
        Short as Short,
        SparseVector as SparseVector,
        Text as Text,
        TokenCount as TokenCount,
    )
    from elasticsearch8_dsl.document import (  # type: ignore[no-redef]
        IndexMeta as IndexMeta,
        DocumentOptions as DocumentOptions,
        DocumentMeta as DocumentMeta,
    )
    from elasticsearch8_dsl.utils import (  # type: ignore[no-redef]
        HitMeta as HitMeta,
        AttrDict as AttrDict,
        META_FIELDS as META_FIELDS,
        DOC_META_FIELDS as DOC_META_FIELDS,
    )
elif _is_installed("elasticsearch7-dsl"):
    from elasticsearch7_dsl import (  # type: ignore[no-redef]
        Document as Document,
        InnerDoc as InnerDoc,
        Index as Index,
        Mapping as Mapping,
        Binary as Binary,
        Boolean as Boolean,
        Byte as Byte,
        Completion as Completion,
        Date as Date,
        DateRange as DateRange,
        Double as Double,
        DoubleRange as DoubleRange,
        Field as Field,
        Float as Float,
        FloatRange as FloatRange,
        HalfFloat as HalfFloat,
        Integer as Integer,
        IntegerRange as IntegerRange,
        Ip as Ip,
        IpRange as IpRange,
        Keyword as Keyword,
        Long as Long,
        LongRange as LongRange,
        Nested as Nested,
        Object as Object,
        RankFeature as RankFeature,
        SearchAsYouType as SearchAsYouType,
        Short as Short,
        SparseVector as SparseVector,
        Text as Text,
        TokenCount as TokenCount,
    )
    from elasticsearch7_dsl.document import (  # type: ignore[no-redef]
        IndexMeta as IndexMeta,
        DocumentOptions as DocumentOptions,
        DocumentMeta as DocumentMeta,
    )
    from elasticsearch7_dsl.utils import (  # type: ignore[no-redef]
        HitMeta as HitMeta,
        AttrDict as AttrDict,
        META_FIELDS as META_FIELDS,
        DOC_META_FIELDS as DOC_META_FIELDS,
    )

    RankFeatures = NotImplemented  # type: ignore
elif _is_installed("elasticsearch6-dsl"):
    from elasticsearch6_dsl import (  # type: ignore[no-redef]
        Document as Document,
        InnerDoc as InnerDoc,
        Index as Index,
        Mapping as Mapping,
        Binary as Binary,
        Boolean as Boolean,
        Byte as Byte,
        Completion as Completion,
        Date as Date,
        DateRange as DateRange,
        Double as Double,
        DoubleRange as DoubleRange,
        Field as Field,
        Float as Float,
        FloatRange as FloatRange,
        HalfFloat as HalfFloat,
        Integer as Integer,
        IntegerRange as IntegerRange,
        Ip as Ip,
        IpRange as IpRange,
        Keyword as Keyword,
        Long as Long,
        LongRange as LongRange,
        Nested as Nested,
        Object as Object,
        Short as Short,
        Text as Text,
        TokenCount as TokenCount,
    )
    from elasticsearch6_dsl.document import (  # type: ignore[no-redef]
        IndexMeta as IndexMeta,
        DocumentOptions as DocumentOptions,
        DocumentMeta as DocumentMeta,
    )
    from elasticsearch6_dsl.utils import (  # type: ignore[no-redef]
        HitMeta as HitMeta,
        AttrDict as AttrDict,
        META_FIELDS as META_FIELDS,
        DOC_META_FIELDS as DOC_META_FIELDS,
    )

    RankFeature = NotImplemented  # type: ignore
    RankFeatures = NotImplemented  # type: ignore
    SearchAsYouType = NotImplemented  # type: ignore
    SparseVector = NotImplemented  # type: ignore
elif _is_installed("elasticsearch-dsl"):
    if not _is_version_at_least("elasticsearch-dsl", "6.0.0"):
        raise ImportError("Elasticsearch DSL version 6.0.0 or higher is required.")
    if _is_version_at_least("elasticsearch-dsl", "8.12.0"):
        raise ImportError("Elasticsearch DSL version below 8.12.0 is required.")
    from elasticsearch_dsl import (  # type: ignore[no-redef,assignment]
        Document as Document,
        InnerDoc as InnerDoc,
        Index as Index,
        Mapping as Mapping,
        Binary as Binary,
        Boolean as Boolean,
        Byte as Byte,
        Completion as Completion,
        Date as Date,
        DateRange as DateRange,
        Double as Double,
        DoubleRange as DoubleRange,
        Field as Field,
        Float as Float,
        FloatRange as FloatRange,
        HalfFloat as HalfFloat,
        Integer as Integer,
        IntegerRange as IntegerRange,
        Ip as Ip,
        IpRange as IpRange,
        Keyword as Keyword,
        Long as Long,
        LongRange as LongRange,
        Nested as Nested,
        Object as Object,
        Short as Short,
        Text as Text,
        TokenCount as TokenCount,
    )
    from elasticsearch_dsl.document import (  # type: ignore[no-redef,assignment,attr-defined]
        IndexMeta as IndexMeta,  # pyright: ignore[reportAttributeAccessIssue]
        DocumentOptions as DocumentOptions,  # pyright: ignore[reportAttributeAccessIssue]
        DocumentMeta as DocumentMeta,  # pyright: ignore[reportAttributeAccessIssue]
    )
    from elasticsearch_dsl.utils import (  # type: ignore[no-redef,assignment]
        HitMeta as HitMeta,
        AttrDict as AttrDict,
        META_FIELDS as META_FIELDS,
        DOC_META_FIELDS as DOC_META_FIELDS,
    )

    if _is_version_at_least("elasticsearch-dsl", "8.0.0"):
        from elasticsearch_dsl import RankFeatures as RankFeatures  # type: ignore[no-redef,assignment]
    else:
        RankFeatures = NotImplemented  # type: ignore[no-redef,assignment]
    if _is_version_at_least("elasticsearch-dsl", "7.0.0"):
        from elasticsearch_dsl import (  # type: ignore[no-redef,assignment]
            RankFeature as RankFeature,
            SearchAsYouType as SearchAsYouType,
            SparseVector as SparseVector,
        )
    else:
        RankFeature = NotImplemented  # type: ignore
        SearchAsYouType = NotImplemented  # type: ignore
        SparseVector = NotImplemented  # type: ignore
else:
    raise ImportError("Elasticsearch DSL is not installed.")
