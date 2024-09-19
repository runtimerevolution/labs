import random
import psycopg
import pytest
from labs.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from labs.rag.embeddings import Embedding
from labs.vector.connect import create_db_connection


def is_postgres_available():
    connection = None
    cursor = None
    try:
        connection = create_db_connection()
        if not connection:
            return False

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        return True
    except Exception as ex:
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@pytest.fixture(scope="session")
def database():
    yield psycopg.connect(
        database=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASS,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
    )


@pytest.fixture(scope="session")
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine(settings.DATABASE_URL, echo=True)
    yield engine_
    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    yield session_
    session_.rollback()
    session_.close()


@pytest.fixture(scope="module")
def create_test_embedding():
    embedding_values = random.sample(range(1, 5000), 1536)

    embedding = Embedding(
        file_and_path="file",
        text="text",
        embedding=embedding_values,
    )
    return [embedding]


@pytest.fixture(scope="module")
def create_test_embeddings():
    embedding_values1 = random.sample(range(1, 5000), 1536)
    embedding1 = Embedding(
        file_and_path="file1",
        text="text1",
        embedding=embedding_values1,
    )
    embedding_values2 = random.sample(range(1, 5000), 1536)
    embedding2 = Embedding(
        file_and_path="file2",
        text="text2",
        embedding=embedding_values2,
    )
    return [embedding1, embedding2]
