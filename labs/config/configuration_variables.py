import os

from logger import setup_logger

setup_logger()


GITHUB_API_BASE_URL = "https://api.github.com"

CLONE_DESTINATION_DIR = os.getenv("CLONE_DESTINATION_DIR", "/tmp/")

DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASS = os.environ.get("DATABASE_PASS", "postgres")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "5432")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "postgres")
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_BACKEND_URL = os.environ.get("CELERY_BACKEND_URL")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

LOCAL_LLM_HOST = os.environ.get("LOCAL_LLM_HOST", "http://ollama:11434")
