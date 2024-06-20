import requests
from .load_access_data import GITHUB_ACCESS_TOKEN
from .load_access_data import GITHUB_OWNER 
from .load_access_data import GITHUB_REPO
from .load_access_data import BASE_URL
from .load_access_data import GITHUB_USERNAME

def get_issues_from_repo():
    url = f'{BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues'
    headers = {
        'Authorization': f'token {GITHUB_ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {
        'assignee': GITHUB_USERNAME,
        'state': 'open',  # You can change this to 'all' or 'closed' as needed
        'per_page': 100,  # Number of results per page (max is 100)
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch issues for {GITHUB_REPO}: {response.status_code} - {response.text}")
        return []