from elasticsearch_pydantic import BaseDocument, BaseInnerDocument


def test_document_from_es() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    hit = {
        "_index": "test-index",
        "_id": "1",
        "_score": 1.0,
        "_source": {
            "title": "Test Document",
            "content": "This is a test document.",
        },
    }
    doc = _Document.from_es(hit)

    assert isinstance(doc, _Document)
    assert doc.index == "test-index"
    assert doc.id == "1"
    assert doc.score == 1.0
    assert doc.title == "Test Document"
    assert doc.content == "This is a test document."


def test_document_model_validate() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    data = {
        "_index": "test-index",
        "_id": "1",
        "_score": 1.0,
        "title": "Test Document",
        "content": "This is a test document.",
    }
    doc = _Document.model_validate(data)

    assert isinstance(doc, _Document)
    assert doc.index == "test-index"
    assert doc.id == "1"
    assert doc.score == 1.0
    assert doc.title == "Test Document"
    assert doc.content == "This is a test document."


def test_inner_document_from_es() -> None:
    class _InnerDocument(BaseInnerDocument):
        title: str
        content: str

    class _Document(BaseDocument):
        name: str
        inner: _InnerDocument

    hit = {
        "_index": "test-index",
        "_id": "1",
        "_score": 1.0,
        "_source": {
            "name": "Outer Document",
            "inner": {
                "title": "Inner Document",
                "content": "This is an inner document.",
            },
        },
    }
    doc = _Document.from_es(hit)

    assert isinstance(doc, _Document)
    assert doc.index == "test-index"
    assert doc.id == "1"
    assert doc.score == 1.0
    assert doc.name == "Outer Document"
    assert isinstance(doc.inner, _InnerDocument)
    assert doc.inner.title == "Inner Document"
    assert doc.inner.content == "This is an inner document."


def test_inner_document_model_validate() -> None:
    class _InnerDocument(BaseInnerDocument):
        title: str
        content: str

    class _Document(BaseDocument):
        name: str
        inner: _InnerDocument

    data = {
        "_index": "test-index",
        "_id": "1",
        "_score": 1.0,
        "name": "Outer Document",
        "inner": {
            "title": "Inner Document",
            "content": "This is an inner document.",
        },
    }
    doc = _Document.model_validate(data)

    assert isinstance(doc, _Document)
    assert doc.index == "test-index"
    assert doc.id == "1"
    assert doc.score == 1.0
    assert doc.name == "Outer Document"
    assert isinstance(doc.inner, _InnerDocument)
    assert doc.inner.title == "Inner Document"
    assert doc.inner.content == "This is an inner document."
