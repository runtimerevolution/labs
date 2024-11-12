import random

from database.connect import db_connector
from database.models import EmbeddingModel
from embeddings.base import Embedder, Embeddings
from embeddings.openai import OpenAIEmbedder
from sqlalchemy import select

from tests.constants import MULTIPLE_EMBEDDINGS, REPO1, SINGLE_EMBEDDING


@db_connector()
def find_embeddings(connection, repository: str):
    query = select(EmbeddingModel).where(EmbeddingModel.repository == repository)
    return connection.execute(query).fetchall()


def test_find_embeddings_no_match(db_session):
    result = find_embeddings(db_session, "")

    assert result == []


def test_find_embeddings_one_match(db_session, create_test_embedding):
    db_session.add_all(create_test_embedding)
    db_session.commit()

    result = find_embeddings(db_session, REPO1)
    assert result != []

    embedding: EmbeddingModel = result[0][0]
    assert embedding.file_path == SINGLE_EMBEDDING["file_path"]
    assert embedding.text == SINGLE_EMBEDDING["text"]
    assert embedding.embedding.size == len(SINGLE_EMBEDDING["embedding"])


def test_find_multiple_embeddings(db_session, create_test_embeddings):
    db_session.add_all(create_test_embeddings)
    db_session.commit()

    result = find_embeddings(db_session, REPO1)
    assert len(result) == 2

    for i in range(len(result)):
        embedding: EmbeddingModel = result[i][0]
        assert embedding.file_path == MULTIPLE_EMBEDDINGS[i]["file_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert embedding.embedding.size == len(MULTIPLE_EMBEDDINGS[i]["embedding"])


def test_reembed_code(db_session):
    files_texts = [("file1", "text1"), ("file2", "text2")]
    embeddings = Embeddings(
        model="model",
        embeddings=[
            random.sample(range(1, 5000), k=1536),
            random.sample(range(1, 5000), k=1536),
        ],
    )

    Embedder(OpenAIEmbedder).reembed_code(
        connection=db_session,
        files_texts=files_texts,
        embeddings=embeddings,
        repository=REPO1,
    )

    result = find_embeddings(db_session, REPO1)
    assert len(result) == 2

    for i in range(len(result)):
        embedding: EmbeddingModel = result[i][0]
        assert embedding.file_path == MULTIPLE_EMBEDDINGS[i]["file_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert embedding.embedding.size == len(MULTIPLE_EMBEDDINGS[i]["embedding"])
