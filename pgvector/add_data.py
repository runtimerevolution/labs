from pgvector.connect import create_db_connection
import psycopg2
from litellm import embedding


def add_data(texts):
    embeddings = embedding(model="text-embedding-ada-002", input=texts)

    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        for text, embedding_obj in zip(texts, embeddings.data):
            cursor.execute(
                "INSERT INTO embeddings (embedding, text) VALUES (%s, %s)",
                (embedding_obj["embedding"], text),
            )
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while writing to DB", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
