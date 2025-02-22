import base64
import logging
import os
from dataclasses import dataclass

import git
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class GithubRequests:
    """Class to handle Github API requests"""

    def __init__(self, token, repository_owner, repository_name, username=None):
        self.token = token
        self.repository_owner = repository_owner
        self.repository_name = repository_name
        self.username = username
        self.github_api_url = f"{settings.GITHUB_API_BASE_URL}/repos/{repository_owner}/{repository_name}"
        self._repository_url = f"{settings.GITHUB_BASE_URL}/{repository_owner}/{repository_name}.git"
        self._directory = f"{settings.CLONE_DESTINATION_DIR}{repository_owner}/{repository_name}"

    @property
    def directory_path(self):
        return self._directory

    @property
    def repository_url(self):
        return self._repository_url

    def _get(self, url, headers={}, params={}):
        try:
            logger.debug(f"Making GET request to {url} with headers {headers} and params {params}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            response_json = response.json()
            logger.debug(f"GET request to {url} successful with response {str(response_json)}")
            return response_json, response.status_code
        except requests.exceptions.RequestException:
            logger.exception("HTTP Request failed.")
        except KeyError:
            logger.exception("Missing key in access data.")
        except Exception:
            logger.exception("An unexpected error occurred.")
        return None, 500

    def _post(self, url, headers={}, data={}):
        try:
            logger.debug(f"Making POST request to {url} with headers {headers} and data {data}")
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()
            logger.debug(f"POST request to {url} successful with response {str(response_json)}")
            return response_json
        except Exception:
            logger.exception("An unexpected error occurred.")
        return None

    def _patch(self, url, headers={}, data={}):
        try:
            logger.debug(f"Making PATCH request to {url} with headers {headers} and data {data}")
            response = requests.patch(url, headers=headers, json=data)
            response_json = response.json()
            logger.debug(f"PATCH request to {url} successful with response {str(response_json)}")
            return response_json
        except Exception:
            logger.exception("An unexpected error occurred.")
        return None

    def list_issues(self, assignee=None, state="open", per_page=100):
        if assignee is None:
            assignee = self.username

        url = f"{self.github_api_url}/issues"

        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        params = {
            "state": state,
            "per_page": per_page,
        }
        if assignee != "all":
            params["assignee"] = assignee

        response_json, _ = self._get(url, headers, params)
        return response_json

    def get_issue(self, issue_number):
        # issue_number is the actual number of the issue, not the id.
        url = f"{self.github_api_url}/issues/{issue_number}"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        response_json, _ = self._get(url, headers, {})
        return response_json

    def create_branch(self, branch_name, original_branch="main"):
        url = f"{self.github_api_url}/git/refs/heads/{original_branch}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Accepted-GitHub-Permissions": "contents=write",
        }
        response_json, status_code = self._get(url, headers=headers)
        if status_code == 200:
            sha = response_json["object"]["sha"]
            create_ref_url = f"{self.github_api_url}/git/refs"
            data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
            return self._post(create_ref_url, headers, data)
        return None

    def change_issue_status(self, issue_number, status):
        if status not in ["open", "closed"]:
            raise ValueError("Invalid state. The state must be 'open' or 'closed'.")

        url = f"{self.github_api_url}/issues/{issue_number}"
        headers = {
            "Authorization": f"token {self.token}",
            "user-agent": "request",
        }
        data = {"state": status}

        return self._patch(url, headers, data)

    def commit_changes(self, message, branch_name, files):
        # Step 1: Get the latest commit SHA on the specified branch
        url = f"{self.github_api_url}/git/refs/heads/{branch_name}"
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json",
        }
        response_json, _ = self._get(url, headers)
        if not response_json:
            return None

        latest_commit_sha = response_json["object"]["sha"]

        # Step 2: Get the tree SHA from the latest commit
        url = f"{self.github_api_url}/git/commits/{latest_commit_sha}"
        response_json, _ = self._get(url, headers)
        if not response_json:
            return None

        base_tree_sha = response_json["tree"]["sha"]

        tree_items = []
        for file_path in files:
            file_name = file_path.replace(f"{self._directory}/", "")
            if file_name.startswith("/"):
                file_name = file_name[1:]

            # Step 3: Read the file content and encode it in Base64
            with open(file_path, "rb") as file:
                file_content = base64.b64encode(file.read()).decode("utf-8")
            # Step 4: Create a new blob for each file
            blob_data = {"content": file_content, "encoding": "base64"}
            blob_url = f"{self.github_api_url}/git/blobs"
            blob_response_json = self._post(blob_url, headers, blob_data)

            blob_sha = blob_response_json["sha"]
            tree_items.append({"path": file_name, "mode": "100644", "type": "blob", "sha": blob_sha})

        # Step 5: Create a new tree with the updated files
        tree_data = {"base_tree": base_tree_sha, "tree": tree_items}
        tree_url = f"{self.github_api_url}/git/trees"
        tree_response_json = self._post(tree_url, headers, tree_data)
        if "status" in tree_response_json:
            logger.error(f"Error while creating tree with updated files: {tree_response_json['message']}")
            return None

        new_tree_sha = tree_response_json["sha"]

        # Step 6: Create a new commit with the new tree
        commit_data = {
            "message": message,
            "parents": [latest_commit_sha],
            "tree": new_tree_sha,
        }
        commit_url = f"{self.github_api_url}/git/commits"
        commit_response_json = self._post(commit_url, headers, commit_data)

        new_commit_sha = commit_response_json["sha"]

        # Step 7: Update the reference of the branch to point to the new commit
        update_ref_data = {"sha": new_commit_sha, "force": False}
        update_ref_url = f"{self.github_api_url}/git/refs/heads/{branch_name}"
        update_ref_response_json = self._patch(update_ref_url, headers, update_ref_data)
        return update_ref_response_json

    def create_pull_request(self, head, base="main", title="New Pull Request", body=""):
        url = f"{self.github_api_url}/pulls"
        headers = {"Authorization": f"token {self.token}"}
        data = {"title": title, "body": body, "head": head, "base": base}
        return self._post(url, headers, data)

    def clone(self):
        try:
            branch = "main"
            probe = f"{self._directory}/.git"
            if not os.path.exists(probe):
                git.Repo.clone_from(self._repository_url, self._directory, branch=branch)
            return self._directory
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None
