from sqlalchemy import text, delete, insert
import logging
from labs.database.connect import db_connector
from labs.database.embeddings import Embedding


logger = logging.getLogger(__name__)


def select_embeddings(session):
    return session.execute(text("SELECT * FROM embeddings;")).fetchall()


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
