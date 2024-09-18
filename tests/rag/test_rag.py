from src.vector.queries import select_embeddings


def test_embeddings_empty(db_session):
    result = select_embeddings()
    assert result == []


def test_embeddings_one(db_session, create_test_embedding):
    db_session.add_all(create_test_embedding)
    db_session.commit()

    result = select_embeddings()
    id, embedding, file_and_path, text, _ = result[0]
    assert id, 1
    assert len(embedding), 1536
    assert file_and_path, "file"
    assert text, "text"


def test_embeddings_multiple(db_session, create_test_embeddings):
    db_session.add_all(create_test_embeddings)
    db_session.commit()

    result = select_embeddings()
    assert len(result), 2

    id, embedding, file_and_path, text, _ = result[0]
    assert id, 1
    assert len(embedding), 1536
    assert file_and_path, "file1"
    assert text, "text1"

    id, embedding, file_and_path, text, _ = result[1]
    assert id, 2
    assert len(embedding), 1536
    assert file_and_path, "file2"
    assert text, "text2"
