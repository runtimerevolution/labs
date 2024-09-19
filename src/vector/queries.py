import psycopg2 as psycopg
from sqlalchemy import Text, text

from src.vector.connect import create_db_connection


create_extension_sql = "CREATE EXTENSION IF NOT EXISTS vector;"
create_table_embeddings_sql = """
CREATE TABLE IF NOT EXISTS embeddings (
  id SERIAL PRIMARY KEY,
  embedding vector,
  file_and_path text,
  text text,
  created_at timestamptz DEFAULT now()
);
"""


def db_connector():
    def decorator(original_function):
        def new_function(*args, **kwargs):
            connection = create_db_connection()
            cursor = connection.cursor()

            try:
                result = original_function(connection, cursor, *args, **kwargs)
                return result
            except (Exception, psycopg.Error) as error:
                print("Error while getting data from DB", error)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

            return result

        return new_function

    return decorator


@db_connector()
def setup_db(connection, cursor):
    cursor.execute(create_extension_sql)
    cursor.execute(create_table_embeddings_sql)
    connection.commit()
    return True


def select_embeddings(session):
    return session.execute(text("SELECT * FROM embeddings;")).fetchall()


@db_connector()
def reembed_code(connection, cursor, files_and_texts, embeddings):
    cursor.execute("DELETE FROM embeddings;")
    connection.commit()

    for text, embedding_obj in zip(files_and_texts, embeddings.data):
        cursor.execute(
            "INSERT INTO embeddings (embedding, file_and_path, text) VALUES (%s, %s, %s)",
            (embedding_obj["embedding"], text[0], text[1]),
        )
    connection.commit()
    return True
