from labs.database.embeddings import Embedding, select_embeddings


def test_select_embeddings_empty(db_session):
    result = select_embeddings(db_session)

    assert result == []


def test_select_embeddings_one(db_session, create_test_embedding):
    db_session.add_all(create_test_embedding)
    db_session.commit()

    result = select_embeddings(db_session)

    embedding: Embedding = result[0][0]
    assert len(embedding.embedding), 1536
    assert embedding.file_and_path, "file"
    assert embedding.text, "text"


def test_select_embeddings_multiple(db_session, create_test_embeddings):
    db_session.add_all(create_test_embeddings)
    db_session.commit()

    result = select_embeddings(db_session)
    assert len(result), 2

    embedding: Embedding = result[0][0]
    assert len(embedding.embedding), 1536
    assert embedding.file_and_path, "file1"
    assert embedding.text, "text1"

    embedding: Embedding = result[1][0]
    assert len(embedding.embedding), 1536
    assert embedding.file_and_path, "file2"
    assert embedding.text, "text2"
