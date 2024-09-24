from litellm import embedding
from sqlalchemy import Column, Integer, String, select
from pgvector.sqlalchemy import Vector

from labs.database.connect import Base, db_connector
import logging


logger = logging.getLogger(__name__)


N_DIM = 1536


class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_and_path = Column(String)
    text = Column(String)
    embedding = Column(Vector(N_DIM))


def insert_embeddings(session, embeddings):
    for emb in embeddings:
        new_embedding = Embedding(embedding=emb)
        session.add(new_embedding)
    session.commit()


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
        .where(
            Embedding.embedding.cosine_distance(query_embedding) < similarity_threshold
        )
        .order_by("distance")
        .limit(10)
    )
    return connection.execute(query).fetchall()
