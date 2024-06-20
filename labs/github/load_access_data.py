import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
GITHUB_ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
GITHUB_OWNER = os.environ['GITHUB_OWNER']
GITHUB_REPO = os.environ['GITHUB_REPO']
GITHUB_USERNAME = os.environ['GITHUB_USERNAME']
BASE_URL = 'https://api.github.com'