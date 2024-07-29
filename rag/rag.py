
from litellm import embedding
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from vector.connect import create_db_connection

Base = declarative_base()
N_DIM = 1536

class Embedding(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_and_path = Column(String)
    text = Column(String)
    embedding = Column(Vector(N_DIM))

def insert_embeddings(session, embeddings):
    for embedding in embeddings:
        new_embedding = Embedding(embedding=embedding)
        session.add(new_embedding)
    session.commit()

def find_similar_embeddings(query):
    k = 5
    similarity_threshold = 0.7

    query = query.replace("\n", "")

    result = embedding(model="text-embedding-ada-002", input=[query])
    query_embedding = result.data[0]["embedding"]

    query = f"""SELECT emb.id, emb.file_and_path, emb.text, (1 - (emb.embedding <=> '{query_embedding}')) AS similarity
        FROM embeddings emb
        WHERE (1 - (emb.embedding <=> '{query_embedding}')) > {similarity_threshold}
        ORDER BY emb.embedding <=> '{query_embedding}'
        LIMIT {k};"""

    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while getting data from DB", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()