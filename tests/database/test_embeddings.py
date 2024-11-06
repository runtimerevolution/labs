import random

from labs.database.embeddings import Embedding, find_embeddings, reembed_code
from tests.constants import MULTIPLE_EMBEDDINGS, REPO1, SINGLE_EMBEDDING


def test_find_embeddings_no_match(db_session):
    result = find_embeddings(db_session, "")

    assert result == []


def test_find_embeddings_one_match(db_session, create_test_embedding):
    db_session.add_all(create_test_embedding)
    db_session.commit()

    result = find_embeddings(db_session, REPO1)
    assert result != []

    embedding: Embedding = result[0][0]
    assert embedding.file_and_path == SINGLE_EMBEDDING["file_and_path"]
    assert embedding.text == SINGLE_EMBEDDING["text"]
    assert embedding.embedding.size == len(SINGLE_EMBEDDING["embedding"])


def test_find_multiple_embeddings(db_session, create_test_embeddings):
    db_session.add_all(create_test_embeddings)
    db_session.commit()

    result = find_embeddings(db_session, REPO1)
    assert len(result) == 2

    for i in range(len(result)):
        embedding: Embedding = result[i][0]
        assert embedding.file_and_path == MULTIPLE_EMBEDDINGS[i]["file_and_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert embedding.embedding.size == len(MULTIPLE_EMBEDDINGS[i]["embedding"])


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

    reembed_code(db_session, files_and_texts, embeddings, REPO1)

    result = find_embeddings(db_session, REPO1)
    assert len(result) == 2

    for i in range(len(result)):
        embedding: Embedding = result[i][0]
        assert embedding.file_and_path == MULTIPLE_EMBEDDINGS[i]["file_and_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert embedding.embedding.size == len(MULTIPLE_EMBEDDINGS[i]["embedding"])
