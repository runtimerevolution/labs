import psycopg2
from pgvector.connect import create_db_connection


def select_embeddings():
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM embeddings;")
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error while getting data from DB", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def reembed_code(files_and_texts, embeddings):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM embeddings;")
        connection.commit()

        for text, embedding_obj in zip(files_and_texts, embeddings.data):
            cursor.execute(
                "INSERT INTO embeddings (embedding, file_and_path, text) VALUES (%s, %s, %s)",
                (embedding_obj["embedding"], text[0], text[1]),
            )
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while writing to DB", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
