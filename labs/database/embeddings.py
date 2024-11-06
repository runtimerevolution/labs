import logging
from typing import List, Tuple

from litellm import embedding
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, delete, insert, select

from labs.database.connect import Base, db_connector

logger = logging.getLogger(__name__)


N_DIM = 1536


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    repository = Column(String)
    file_and_path = Column(String)
    text = Column(String)
    embedding = Column(Vector(N_DIM))


@db_connector()
def find_embeddings(connection, repository: str):
    query = select(Embedding).where(Embedding.repository == repository)
    return connection.execute(query).fetchall()


@db_connector()
def find_similar_embeddings(connection, query):
    similarity_threshold = 0.7

    query = query.replace("\n", "")

    result = embedding(model="text-embedding-ada-002", input=[query])
    query_embedding = result.data[0]["embedding"]

    query = (
        select(
            Embedding,
            Embedding.embedding.cosine_distance(query_embedding).label("distance"),
        )
        .where(Embedding.embedding.cosine_distance(query_embedding) < similarity_threshold)
        .order_by("distance")
        .limit(10)
    )
    return connection.execute(query).fetchall()


@db_connector()
def reembed_code(connection, files_and_texts: List[Tuple[str, str]], embeddings, repository: str):
    query = delete(Embedding).where(Embedding.repository == repository)
    connection.execute(query)

    for gen_text, embedding_obj in zip(files_and_texts, embeddings.data):
        query = insert(Embedding).values(
            repository=repository,
            embedding=embedding_obj["embedding"],
            file_and_path=gen_text[0],
            text=gen_text[1],
        )
        connection.execute(query)
    connection.commit()
    return True
