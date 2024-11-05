import random

from sqlalchemy import select

from labs.database.connect import db_connector
from labs.database.models import EmbeddingModel
from labs.embeddings.base import Embedder, Embeddings
from labs.embeddings.openai import OpenAIEmbedder


@db_connector()
def select_embeddings(connection):
    query = select(EmbeddingModel)
    return connection.execute(query).fetchall()


def test_select_embeddings_empty(db_session):
    result = select_embeddings(db_session)

    assert result == []


def test_select_embeddings_one(db_session, create_test_embedding):
    db_session.add_all(create_test_embedding)
    db_session.commit()

    result = select_embeddings(db_session)

    embedding: EmbeddingModel = result[0][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_path == "file1"
    assert embedding.text == "text1"


def test_select_embeddings_multiple(db_session, create_test_embeddings):
    db_session.add_all(create_test_embeddings)
    db_session.commit()

    result = select_embeddings(db_session)
    assert len(result) == 2

    embedding: EmbeddingModel = result[0][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_path == "file1"
    assert embedding.text == "text1"

    embedding: EmbeddingModel = result[1][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_path == "file2"
    assert embedding.text == "text2"


def test_reembed_code(db_session):
    files_texts = [("file1", "text1"), ("file2", "text2")]
    embeddings = Embeddings(
        model="model", embeddings=[random.sample(range(1, 5000), k=1536), random.sample(range(1, 5000), k=1536)]
    )

    Embedder(OpenAIEmbedder).reembed_code(connection=db_session, files_texts=files_texts, embeddins=embeddings)

    result = select_embeddings(db_session)
    assert len(result) == 2

    embedding: EmbeddingModel = result[0][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_path == "file1"
    assert embedding.text == "text1"

    embedding: EmbeddingModel = result[1][0]
    assert len(embedding.embedding) == 1536
    assert embedding.file_path == "file2"
    assert embedding.text == "text2"
