import os
from pathlib import Path


# Paths
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

TEST_ENVIRONMENT = eval(os.environ.get("TEST_ENVIRONMENT", False))

LITELLM_MASTER_KEY = os.environ.get("LITELLM_MASTER_KEY")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY")


CLONE_DESTINATION_DIR = os.getenv("CLONE_DESTINATION_DIR", "/tmp/")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "openai/gpt-3.5-turbo")

ACTIVELOOP_TOKEN = os.environ["ACTIVELOOP_TOKEN"]

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


ACTIVELOOP_TOKEN = os.environ.get("ACTIVELOOP_TOKEN")

DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASS = os.environ.get("DATABASE_PASS")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_URL = os.environ.get("DATABASE_URL")

DATABASE_TEST_HOST = os.environ.get("DATABASE_TEST_HOST")
DATABASE_TEST_USER = os.environ.get("DATABASE_TEST_USER")
DATABASE_TEST_PASS = os.environ.get("DATABASE_TEST_PASS")
DATABASE_TEST_NAME = os.environ.get("DATABASE_TEST_NAME")
DATABASE_TEST_PORT = os.environ.get("DATABASE_TEST_PORT")
DATABASE_TEST_URL = os.environ.get("DATABASE_TEST_URL")

POLYGLOT_DIR = PROJ_ROOT / "labs" / "polyglot_data"

spacy_models = [
    {"language_code": "pt", "language_name": "portuguese", "model": "pt_core_news_lg"},
    {"language_code": "en", "language_name": "english", "model": "en_core_web_md"},
]

SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
