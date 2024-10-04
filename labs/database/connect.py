from labs.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging


logger = logging.getLogger(__name__)


engine = create_engine(settings.DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def db_connector():
    def decorator(original_function):
        def new_function(*args, **kwargs):
            if settings.TEST_ENVIRONMENT:
                return original_function(*args, **kwargs)

            connection = engine.connect()

            try:
                return original_function(connection, *args, **kwargs)
            except Exception:
                logger.exception("Error while getting data from DB.")
            finally:
                if connection:
                    connection.close()

            return None

        return new_function

    return decorator
