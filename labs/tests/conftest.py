from typing import List

# import config.configuration_variables as settings
import pytest
from embeddings.models import Embedding

# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
from tests.constants import MULTIPLE_EMBEDDINGS, SINGLE_EMBEDDING

# engine = create_engine(settings.DATABASE_URL, echo=True)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()


# @pytest.fixture(scope="function")
# def db_session():
#     """yields a SQLAlchemy connection which is rollbacked after the test
#     https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
#     """
#     connection = engine.connect()
#     # begin a non-ORM transaction
#     trans = connection.begin()
#     # bind an individual Session to the connection, selecting
#     # "create_savepoint" join_transaction_mode
#     session = Session(bind=connection, join_transaction_mode="create_savepoint")
#
#     yield session
#
#     session.close()
#     trans.rollback()
#     connection.close()


@pytest.fixture
@pytest.mark.django_db
def create_test_embedding():
    embedding = Embedding(**SINGLE_EMBEDDING)
    embedding.save()

    return [embedding]


@pytest.fixture
@pytest.mark.django_db
def create_test_embeddings():
    embeddings: List[Embedding] = []

    for embedding in MULTIPLE_EMBEDDINGS:
        embeddings.append(Embedding(**embedding))

    Embedding.objects.bulk_create(embeddings)
    return embeddings
