import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from pythonjsonlogger import jsonlogger

# Load environment variables from .env file if it exists
load_dotenv(dotenv_path=".env")

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.propagate = False

logger.debug(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"
REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
GITHUB_OWNER = os.environ["GITHUB_OWNER"]
GITHUB_REPO = os.environ["GITHUB_REPO"]
GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_API_BASE_URL = "https://api.github.com"

LITELLM_MASTER_KEY = os.environ["LITELLM_MASTER_KEY"]
LITELLM_API_KEY = os.environ["LITELLM_API_KEY"]

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
COHERE_API_KEY = os.environ["COHERE_API_KEY"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

CLONE_DESTINATION_DIR = os.getenv("CLONE_DESTINATION_DIR", "/tmp/")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "openai/gpt-3.5-turbo")

ACTIVELOOP_TOKEN = os.environ["ACTIVELOOP_TOKEN"]

DATABASE_URL = os.environ["DATABASE_URL"]

POLYGLOT_DIR = PROJ_ROOT / "labs" / "polyglot_data"

spacy_models = [
    {"language_code": "pt", "language_name": "portuguese", "model": "pt_core_news_lg"},
    {"language_code": "en", "language_name": "english", "model": "en_core_web_md"},
]

SUMMARIZATION_MODEL = "facebook/bart-large-cnn"


def get_logger(module_name):
    return logging.getLogger(module_name)
