import psycopg2 as psycopg


from labs.config import settings


def create_db_connection():
    try:
        return psycopg.connect(
            host=settings.DATABASE_HOST,
            database=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASS,
            port=settings.DATABASE_PORT,
        )
    except (Exception, psycopg.Error) as error:
        print("Error while connecting", error)
    return None
