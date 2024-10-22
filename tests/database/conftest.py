import random
import pytest
from config import configuration_variables as settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from labs.database.embeddings import Embedding


engine = create_engine(settings.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


@pytest.fixture(scope="function")
def db_session():
    """yields a SQLAlchemy connection which is rollbacked after the test
    https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    connection = engine.connect()
    # begin a non-ORM transaction
    trans = connection.begin()
    # bind an individual Session to the connection, selecting
    # "create_savepoint" join_transaction_mode
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope="module")
def create_test_embedding():
    embedding_values = random.sample(range(1, 5000), 1536)

    embedding = Embedding(
        file_and_path="file1",
        text="text1",
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
