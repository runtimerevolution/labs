import base64
import requests
from dataclasses import dataclass
import logging
import git
import os

logger = logging.getLogger(__name__)


@dataclass
class GithubRequests:
    """Class to handle Github API requests"""

    def __init__(self, github_token, repo_owner, repo_name, user_name=None):

        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.username = user_name
        self.github_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.directory_dir = f"/tmp/{self.repo_owner}/{self.repo_name}"

    logger = logging.getLogger(__name__)

    def list_issues(self, assignee=None, state="open", per_page=100):
        if assignee is None:
            assignee = self.username
        try:
            url = f"{self.github_api_url}/issues"

            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            params = {
                "state": state,
                "per_page": per_page,
            }
            if assignee != "all":
                params["assignee"] = assignee

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

    def get_issue(self, issue_number):
        # issue number is the actual number of the issue, not the id
        try:
            url = f"{self.github_api_url}/issues/{issue_number}"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json",
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

    def create_branch(self, branch_name, original_branch="main"):
        url = f"{self.github_api_url}/git/refs/heads/{original_branch}"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "X-Accepted-GitHub-Permissions": "contents=write",
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                sha = response.json()["object"]["sha"]
                create_ref_url = f"{self.github_api_url}/git/refs"
                data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
                create_response = requests.post(
                    create_ref_url, headers=headers, json=data
                )
                return create_response.json()

            else:
                self.logger.error(f"Error getting: {response}")
                return None

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return None

    def change_issue_status(self, issue_number, state):
        if state not in ["open", "closed"]:
            raise ValueError("Invalid state. The state must be 'open' or 'closed'.")

        url = f"{self.github_api_url}/issues/{issue_number}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "user-agent": "request",
        }
        data = {"state": state}
        response = requests.patch(url, headers=headers, json=data)
        return response.json()

    def commit_changes(self, message, branch_name, files):
        # Step 1: Get the latest commit SHA on the specified branch
        url = f"{self.github_api_url}/git/refs/heads/{branch_name}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.logger.error(f"Error getting: {response}")
            return None

        latest_commit_sha = response.json()["object"]["sha"]

        # Step 2: Get the tree SHA from the latest commit
        url = f"{self.github_api_url}/git/commits/{latest_commit_sha}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.logger.error(f"Error getting: {response}")
            return None

        base_tree_sha = response.json()["tree"]["sha"]

        tree_items = []
        for file_path in files:

            file_name = file_path.replace(f"{self.directory_dir}/", "")
            # Step 3: Read the file content and encode it in Base64
            with open(file_path, "rb") as file:
                file_content = base64.b64encode(file.read()).decode("utf-8")
            # Step 4: Create a new blob for each file
            blob_data = {"content": file_content, "encoding": "base64"}
            blob_url = f"{self.github_api_url}/git/blobs"
            blob_response = requests.post(blob_url, headers=headers, json=blob_data)
            blob_sha = blob_response.json()["sha"]

            tree_items.append(
                {"path": file_name, "mode": "100644", "type": "blob", "sha": blob_sha}
            )
        # Step 5: Create a new tree with the updated files
        tree_data = {"base_tree": base_tree_sha, "tree": tree_items}
        tree_url = f"{self.github_api_url}/git/trees"
        tree_response = requests.post(tree_url, headers=headers, json=tree_data)
        new_tree_sha = tree_response.json()["sha"]

        # Step 6: Create a new commit with the new tree
        commit_data = {
            "message": message,
            "parents": [latest_commit_sha],
            "tree": new_tree_sha,
        }
        commit_url = f"{self.github_api_url}/git/commits"
        commit_response = requests.post(commit_url, headers=headers, json=commit_data)
        new_commit_sha = commit_response.json()["sha"]

        # Step 7: Update the reference of the branch to point to the new commit
        update_ref_data = {"sha": new_commit_sha, "force": False}
        update_ref_url = f"{self.github_api_url}/git/refs/heads/{branch_name}"
        update_ref_response = requests.patch(
            update_ref_url, headers=headers, json=update_ref_data
        )
        return update_ref_response.json()

    def create_pull_request(self, head, base="main", title="New Pull Request", body=""):
        url = f"{self.github_api_url}/pulls"
        headers = {"Authorization": f"token {self.github_token}"}
        data = {"title": title, "body": body, "head": head, "base": base}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def clone(self):
        try:
            url = f"https://github.com/{self.repo_owner}/{self.repo_name}.git"
            branch = "main"
            probe = f"/tmp/{self.repo_owner}/{self.repo_name}/.git"
            if not os.path.exists(probe):
                cloned_repo = git.Repo.clone_from(
                    url, self.directory_dir, branch=branch
                )
            return self.directory_dir
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return None
