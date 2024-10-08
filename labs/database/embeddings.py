from litellm import embedding
from sqlalchemy import Column, Integer, String, select
from pgvector.sqlalchemy import Vector

from labs.database.connect import Base, db_connector
import logging
from sqlalchemy import delete, insert


logger = logging.getLogger(__name__)


N_DIM = 1536


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_and_path = Column(String)
    text = Column(String)
    embedding = Column(Vector(N_DIM))


@db_connector()
def select_embeddings(connection):
    query = select(Embedding)
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
def reembed_code(connection, files_and_texts, embeddings):
    query = delete(Embedding)
    connection.execute(query)
    for gen_text, embedding_obj in zip(files_and_texts, embeddings.data):
        query = insert(Embedding).values(
            embedding=embedding_obj["embedding"],
            file_and_path=gen_text[0],
            text=gen_text[1],
        )
        connection.execute(query)
    connection.commit()
    return True
