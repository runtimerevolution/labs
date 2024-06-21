import requests
from labs.config import GITHUB_ACCESS_TOKEN
from labs.config import GITHUB_API_BASE_URL
from labs.config import GITHUB_OWNER
from labs.config import GITHUB_REPO
from labs.config import get_logger

logger = get_logger(__name__)

def get_issue(issue_id):
    try:
        url = f'{GITHUB_API_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{issue_id}'
        headers = {
            'Authorization': f'token {GITHUB_ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(str(response_json))
        return response_json

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
        return None
    except KeyError as e:
        logger.error(f"Missing key in access data: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

def issue_body(issue):
    try:
        body = issue['body']
        return body
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None