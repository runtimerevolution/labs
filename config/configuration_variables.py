import os
from pathlib import Path

from labs.logger import setup_logger


setup_logger()


PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"
REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")
GITHUB_OWNER = os.environ.get("GITHUB_OWNER")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_API_BASE_URL = "https://api.github.com"

TEST_ENVIRONMENT = eval(os.environ.get("TEST_ENVIRONMENT", "False"))

LITELLM_MASTER_KEY = os.environ.get("LITELLM_MASTER_KEY")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY")

CLONE_DESTINATION_DIR = os.getenv("CLONE_DESTINATION_DIR", "/tmp/")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "openai/gpt-4o")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

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

LOCAL_LLM = eval(os.environ.get("LOCAL_LLM", "False"))
LOCAL_EMBEDDER = eval(os.environ.get("LOCAL_EMBEDDER", "False"))
LOCAL_LLM_HOST = os.environ.get("LOCAL_LLM_HOST", "http://ollama:11434")
