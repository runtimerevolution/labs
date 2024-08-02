import psycopg2
from labs.config import (
    TEST_ENVIRONMENT,
    DATABASE_HOST,
    DATABASE_USER,
    DATABASE_PASS,
    DATABASE_NAME,
    DATABASE_PORT,
    DATABASE_TEST_HOST,
    DATABASE_TEST_USER,
    DATABASE_TEST_PASS,
    DATABASE_TEST_NAME,
    DATABASE_TEST_PORT,
)


def db_config():
    return {
        "host": DATABASE_HOST,
        "database": DATABASE_NAME,
        "user": DATABASE_USER,
        "password": DATABASE_PASS,
        "port": DATABASE_PORT,
    }


def db_test_config():
    return {
        "host": DATABASE_TEST_HOST,
        "database": DATABASE_TEST_NAME,
        "user": DATABASE_TEST_USER,
        "password": DATABASE_TEST_PASS,
        "port": DATABASE_TEST_PORT,
    }


def create_db_connection():
    if TEST_ENVIRONMENT:
        params = db_test_config()
    else:
        params = db_config()

    try:
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting", error)
    return None
