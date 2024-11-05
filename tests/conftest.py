import random

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import configuration_variables as settings
from labs.database.models import EmbeddingModel

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

    embedding = EmbeddingModel(
        file_path="file",
        text="text",
        embedding=embedding_values,
    )
    return [embedding]


@pytest.fixture(scope="module")
def create_test_embeddings():
    embedding_values1 = random.sample(range(1, 5000), 1536)
    embedding1 = EmbeddingModel(
        file_path="file1",
        text="text1",
        embedding=embedding_values1,
    )
    embedding_values2 = random.sample(range(1, 5000), 1536)
    embedding2 = EmbeddingModel(
        file_path="file2",
        text="text2",
        embedding=embedding_values2,
    )
    return [embedding1, embedding2]
