from django.core.management.base import BaseCommand
from config.models import Config
from config.lite_llm_database_config import load_config_from_db, rewrite_config_yaml

class Command(BaseCommand):
  help = 'Reload API Keys for lite llm from the database'
