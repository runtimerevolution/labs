import time

import docker
import psycopg
import pytest
from pytest_postgresql.janitor import DatabaseJanitor
from labs.config import (
    DATABASE_TEST_PASS,
    DATABASE_TEST_PORT,
    DATABASE_TEST_USER,
    DATABASE_TEST_NAME,
)


@pytest.fixture(scope="session")
def psql_docker():
    client = docker.from_env()
    container = client.containers.run(
        image="ankane/pgvector",
        auto_remove=True,
        environment=dict(
            POSTGRES_USER=DATABASE_TEST_USER,
            POSTGRES_PASSWORD=DATABASE_TEST_PASS,
        ),
        name=DATABASE_TEST_NAME,
        ports={"5432/tcp": ("127.0.0.1", DATABASE_TEST_PORT)},
        detach=True,
        remove=True,
    )
    # Wait for the container to start.
    time.sleep(15)

    yield

    container.stop()


@pytest.fixture(scope="session")
def database(psql_docker):
    with DatabaseJanitor(
        user=DATABASE_TEST_USER,
        host="localhost",
        port=DATABASE_TEST_PORT,
        dbname=DATABASE_TEST_NAME,
        password=DATABASE_TEST_PASS,
        version="0.5.1",
    ):
        yield psycopg.connect(
            dbname=DATABASE_TEST_NAME,
            user=DATABASE_TEST_USER,
            password=DATABASE_TEST_PASS,
            host="localhost",
            port=DATABASE_TEST_PORT,
        )
