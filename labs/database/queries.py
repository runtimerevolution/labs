import psycopg2 as psycopg
from sqlalchemy import text
import logging

from labs.database.connect import create_db_connection

logger = logging.getLogger(__name__)


def db_connector():
    def decorator(original_function):
        def new_function(*args, **kwargs):
            connection = create_db_connection()
            cursor = connection.cursor()

            try:
                result = original_function(connection, cursor, *args, **kwargs)
                return result
            except (Exception, psycopg.Error):
                logger.exception("Error while getting data from DB.")
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

            return result

        return new_function

    return decorator


def select_embeddings(session):
    return session.execute(text("SELECT * FROM embeddings;")).fetchall()


@db_connector()
def reembed_code(connection, cursor, files_and_texts, embeddings):
    cursor.execute("DELETE FROM embeddings;")
    connection.commit()

    for gen_text, embedding_obj in zip(files_and_texts, embeddings.data):
        cursor.execute(
            "INSERT INTO embeddings (embedding, file_and_path, text) VALUES (%s, %s, %s)",
            (embedding_obj["embedding"], gen_text[0], gen_text[1]),
        )
    connection.commit()
    return True
