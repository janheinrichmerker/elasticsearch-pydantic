from elasticsearch_pydantic import BaseDocument, BaseInnerDocument


def test_document_to_dict() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    doc_dict = doc.to_dict(include_meta=False)

    assert isinstance(doc_dict, dict)
    assert doc_dict == {
        "title": "Test Document",
        "content": "This is a test document.",
    }


def test_document_to_dict_meta() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    doc_dict = doc.to_dict(include_meta=True)

    assert isinstance(doc_dict, dict)
    assert doc_dict == {
        "_index": "test-index",
        "_id": "1",
        "_source": {
            "title": "Test Document",
            "content": "This is a test document.",
        },
    }


def test_document_to_dict_empty() -> None:
    class _Document(BaseDocument):
        title: str
        content: str
        optional_field: str | None = None

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    doc_dict = doc.to_dict(include_meta=False, skip_empty=True)

    assert isinstance(doc_dict, dict)
    assert doc_dict == {
        "title": "Test Document",
        "content": "This is a test document.",
    }


def test_document_index_action() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    action = doc.index_action()

    assert isinstance(action, dict)
    assert action == {
        "_index": "test-index",
        "_id": "1",
        "_op_type": "index",
        "title": "Test Document",
        "content": "This is a test document.",
    }


def test_document_create_action() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    action = doc.create_action()

    assert isinstance(action, dict)
    assert action == {
        "_index": "test-index",
        "_id": "1",
        "_op_type": "create",
        "title": "Test Document",
        "content": "This is a test document.",
    }


def test_document_update_action() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    action = doc.update_action(content="Updated content.")

    assert isinstance(action, dict)
    assert action == {
        "_index": "test-index",
        "_id": "1",
        "_op_type": "update",
        "doc": {
            "content": "Updated content.",
        },
    }


def test_document_update_action_retry() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    action = doc.update_action(content="Updated content.", retry_on_conflict=3)

    assert isinstance(action, dict)
    assert action == {
        "_index": "test-index",
        "_id": "1",
        "_op_type": "update",
        "retry_on_conflict": 3,
        "doc": {
            "content": "Updated content.",
        },
    }


def test_document_delete_action() -> None:
    class _Document(BaseDocument):
        title: str
        content: str

    doc = _Document(
        index="test-index",
        id="1",
        title="Test Document",
        content="This is a test document.",
    )
    action = doc.delete_action()

    assert isinstance(action, dict)
    assert action == {
        "_index": "test-index",
        "_id": "1",
        "_op_type": "delete",
    }
