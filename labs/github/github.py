import requests
from labs.config import GITHUB_ACCESS_TOKEN
from labs.config import GITHUB_API_BASE_URL
from labs.config import GITHUB_OWNER
from labs.config import GITHUB_REPO
from labs.config import GITHUB_USERNAME
from labs.config import get_logger

class Github:
    def __init__(self, access_token=GITHUB_ACCESS_TOKEN, api_base_url=GITHUB_API_BASE_URL, 
                 owner=GITHUB_OWNER, repo=GITHUB_REPO, username=GITHUB_USERNAME):
        self.access_token = access_token
        self.api_base_url = api_base_url
        self.owner = owner
        self.repo = repo
        self.username = username
        self.logger = get_logger(__name__)

    def get_issues_from_repo(self, assignee=None, state='open', per_page=100):
        if assignee is None:
            assignee = self.username
        try:
            url = f'{self.api_base_url}/repos/{self.owner}/{self.repo}/issues'
            headers = {
                'Authorization': f'token {self.access_token}',
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
            self.logger.debug(str(response_json))
            return response_json

        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP Request failed: {e}")
        except KeyError as e:
            self.logger.error(f"Missing key in access data: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
        return []

    def get_issue(self, issue_id):
        try:
            url = f'{self.api_base_url}/repos/{self.owner}/{self.repo}/issues/{issue_id}'
            headers = {
                'Authorization': f'token {self.access_token}',
                'Accept': 'application/vnd.github.v3+json',
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            self.logger.debug(str(response_json))
            return response_json

        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP Request failed: {e}")
            return None
        except KeyError as e:
            self.logger.error(f"Missing key in access data: {e}")
            return None
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return None

    def issue_body(self, issue):
        try:
            body = issue['body']
            return body
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return None
