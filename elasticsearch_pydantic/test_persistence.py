from unittest.mock import Mock

from pytest import raises

from elasticsearch_pydantic import BaseDocument
from elasticsearch_pydantic._compat import Elasticsearch


def _mock_elasticsearch() -> Mock:
    es = Mock(spec=Elasticsearch)
    es.index.return_value = {
        "_index": "test-index",
        "_id": "1",
        "_version": 1,
        "result": "created",
    }
    es.delete.return_value = {"result": "deleted"}
    return es


def test_document_save() -> None:
    class _Document(BaseDocument):
        title: str

    es = _mock_elasticsearch()
    doc = _Document(title="Test Document")
    result = doc.save(using=es, index="test-index")

    # Elasticsearch DSL 6 returns a boolean instead of the result string.
    assert result in ("created", True)
    es.index.assert_called_once()
    params = es.index.call_args.kwargs
    assert params["index"] == "test-index"
    body = params.get("document", params.get("body"))
    assert body == {"title": "Test Document"}


def test_document_save_updates_meta() -> None:
    class _Document(BaseDocument):
        title: str

    es = _mock_elasticsearch()
    doc = _Document(title="Test Document")
    doc.save(using=es, index="test-index")

    assert doc.id == "1"
    assert doc.index == "test-index"
    assert doc.version == 1
    assert doc.meta.id == "1"


def test_document_delete() -> None:
    class _Document(BaseDocument):
        title: str

    es = _mock_elasticsearch()
    doc = _Document(id="1", title="Test Document")
    doc.delete(using=es, index="test-index")

    es.delete.assert_called_once()
    params = es.delete.call_args.kwargs
    assert params["index"] == "test-index"
    assert params["id"] == "1"


def test_document_update_not_implemented() -> None:
    class _Document(BaseDocument):
        title: str

    es = _mock_elasticsearch()
    doc = _Document(id="1", title="Test Document")
    with raises(NotImplementedError):
        doc.update(using=es, index="test-index", title="Updated")

    assert not es.method_calls
