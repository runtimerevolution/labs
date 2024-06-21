import requests
from labs.config import GITHUB_ACCESS_TOKEN
from labs.config import GITHUB_API_BASE_URL
from labs.config import GITHUB_OWNER
from labs.config import GITHUB_REPO
from labs.config import GITHUB_USERNAME
from labs.config import get_logger

logger = get_logger(__name__)

def get_issues_from_repo(assignee=GITHUB_USERNAME, state='open', per_page=100):
    try:
        url = f'{GITHUB_API_BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues'
        headers = {
            'Authorization': f'token {GITHUB_ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
        }
        params = {
            'state': state,
            'per_page': per_page,
        }
        if assignee != 'all':
            params['assignee'] = assignee
            
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(str(response_json))
        return response_json

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
    except KeyError as e:
        logger.error(f"Missing key in access data: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    return []
