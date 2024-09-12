import time
import random
import docker
import psycopg2
import pytest

from labs.config import (
    DATABASE_TEST_PASS,
    DATABASE_TEST_PORT,
    DATABASE_TEST_USER,
    DATABASE_TEST_NAME,
)
from vector.connect import create_db_connection
from vector.queries import setup_db
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from labs.config import DATABASE_TEST_URL
from rag.embeddings import Embedding


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
def psql_docker():
    client = docker.from_env()
    container = client.containers.run(
        image="ankane/pgvector",
        auto_remove=True,
        environment=dict(
            POSTGRES_DB=DATABASE_TEST_NAME,
            POSTGRES_USER=DATABASE_TEST_USER,
            POSTGRES_PASSWORD=DATABASE_TEST_PASS,
            POSTGRES_HOST_AUTH_METHOD="trust",
        ),
        name=DATABASE_TEST_NAME,
        ports={"5432/tcp": ("127.0.0.1", DATABASE_TEST_PORT)},
        detach=True,
        remove=True,
        volumes=[
            "vector.scripts:/docker-entrypoint-initdb.d",
        ],
    )

    timeout = 10

    start = time.time()
    while container.status != "running":
        container.reload()
        elapsed = time.time() - start
        if elapsed > timeout:
            raise Exception

    start = time.time()
    while not is_postgres_available():
        elapsed = time.time() - start
        if elapsed > timeout:
            raise Exception

    setup_db()

    yield

    container.stop()


@pytest.fixture(scope="session")
def database(psql_docker):
    yield psycopg2.connect(
        database=DATABASE_TEST_NAME,
        user=DATABASE_TEST_USER,
        password=DATABASE_TEST_PASS,
        host="localhost",
        port=DATABASE_TEST_PORT,
    )


@pytest.fixture(scope="session")
def db_engine(psql_docker, request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine(DATABASE_TEST_URL, echo=True)
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
