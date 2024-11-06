from typing import List
import pytest
from config import configuration_variables as settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from labs.database.embeddings import Embedding
from tests.constants import MULTIPLE_EMBEDDINGS, SINGLE_EMBEDDING


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
    embedding = Embedding(**SINGLE_EMBEDDING)
    return [embedding]


@pytest.fixture(scope="module")
def create_test_embeddings():
    embeddings: List[Embedding] = []

    for embedding in MULTIPLE_EMBEDDINGS:
        embeddings.append(Embedding(**embedding))

    return embeddings
