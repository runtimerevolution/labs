from labs.database.embeddings import Embedding, select_embeddings, reembed_code
import random


def test_select_embeddings_empty(db_session):
    result = select_embeddings(db_session)

    assert result == []


def test_select_embeddings_one(db_session, create_test_embedding):
    db_session.add_all(create_test_embedding)
    db_session.commit()

    result = select_embeddings(db_session)

    embedding: Embedding = result[0][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_and_path == "file1"
    assert embedding.text == "text1"


def test_select_embeddings_multiple(db_session, create_test_embeddings):
    db_session.add_all(create_test_embeddings)
    db_session.commit()

    result = select_embeddings(db_session)
    assert len(result) == 2

    embedding: Embedding = result[0][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_and_path == "file1"
    assert embedding.text == "text1"

    embedding: Embedding = result[1][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_and_path == "file2"
    assert embedding.text == "text2"


def test_reembed_code(db_session):
    files_and_texts = [("file1", "text1"), ("file2", "text2")]
    embeddings = type(
        "obj",
        (object,),
        {
            "data": [
                {"embedding": random.sample(range(1, 5000), 1536)},
                {"embedding": random.sample(range(1, 5000), 1536)},
            ]
        },
    )

    reembed_code(db_session, files_and_texts, embeddings)

    result = select_embeddings(db_session)
    assert len(result) == 2

    embedding: Embedding = result[0][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_and_path == "file1"
    assert embedding.text == "text1"

    embedding: Embedding = result[1][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_and_path == "file2"
    assert embedding.text == "text2"
