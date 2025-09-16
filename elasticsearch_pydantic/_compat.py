from typing import Optional

from elastic_transport._response import ObjectApiResponse as ObjectApiResponse


# Elasticsearch DSL imports (will use major-version-locked package or default)
_import_error: Optional[ImportError] = ImportError()
if _import_error is not None:
    # elasticsearch8-dsl<8.18.0
    try:
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

        ConstantKeyword = NotImplemented  # type: ignore

        _import_error = None
    except ImportError as e:
        _import_error = e
if _import_error is not None:
    # elasticsearch7-dsl
    try:
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

        ConstantKeyword = NotImplemented  # type: ignore
        RankFeatures = NotImplemented  # type: ignore

        _import_error = None
    except ImportError as e:
        _import_error = e
if _import_error is not None:
    # elasticsearch6-dsl
    try:
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

        ConstantKeyword = NotImplemented  # type: ignore
        RankFeature = NotImplemented  # type: ignore
        RankFeatures = NotImplemented  # type: ignore
        SearchAsYouType = NotImplemented  # type: ignore
        SparseVector = NotImplemented  # type: ignore

        _import_error = None
    except ImportError as e:
        _import_error = e
if _import_error is not None:
    # elasticsearch-dsl<8.18.0
    try:
        from elasticsearch_dsl import (  # type: ignore[no-redef,assignment]
            Document as Document,
            InnerDoc as InnerDoc,
            Index as Index,
            Mapping as Mapping,
            Binary as Binary,
            Boolean as Boolean,
            Byte as Byte,
            Completion as Completion,
            ConstantKeyword as ConstantKeyword,
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

        _import_error = None
    except ImportError as e:
        _import_error = e
if _import_error is not None:
    raise _import_error
