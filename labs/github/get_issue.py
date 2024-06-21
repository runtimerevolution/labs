import requests
from .load_access_data import load_access_data

def get_issue(issue_id):
    try:
        access_data = load_access_data()
        GITHUB_ACCESS_TOKEN = access_data['GITHUB_ACCESS_TOKEN']
        BASE_URL = access_data['BASE_URL']
        GITHUB_OWNER = access_data['GITHUB_OWNER']
        GITHUB_REPO = access_data['GITHUB_REPO']
        
        url = f'{BASE_URL}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues/{issue_id}'
        headers = {
            'Authorization': f'token {GITHUB_ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except KeyError as e:
        print(f"Missing key in access data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def issue_body(issue):
    try:
        body = issue['body']
        return body
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None