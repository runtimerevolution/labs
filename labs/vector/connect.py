import psycopg2 as psycopg


from labs.config import settings


def db_config():
    return {
        "host": settings.DATABASE_HOST,
        "database": settings.DATABASE_NAME,
        "user": settings.DATABASE_USER,
        "password": settings.DATABASE_PASS,
        "port": settings.DATABASE_PORT,
    }


def create_db_connection():
    params = db_config()

    try:
        conn = psycopg.connect(**params)
        return conn
    except (Exception, psycopg.Error) as error:
        print("Error while connecting", error)
    return None
