import os

import requests
from github.github import GithubRequests


class TestGithubRequests:
    # Listing issues with default parameters returns open issues assigned to the user
    def test_list_issues_default_parameters(self, mocker):
        mock_get = mocker.patch("requests.get")

        sample_response = [
            {"id": 1, "title": "Issue 1", "state": "open"},
            {"id": 2, "title": "Issue 2", "state": "open"},
        ]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response

        token = "valid_token"
        repository_owner = "owner_username"
        repository_name = "repository_name"
        username = "your_username"
        github_requests = GithubRequests(token, repository_owner, repository_name, username)

        issues = github_requests.list_issues()

        assert issues == sample_response
        mock_get.assert_called_once_with(
            f"https://api.github.com/repos/{repository_owner}/{repository_name}/issues",
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            params={
                "state": "open",
                "per_page": 100,
                "assignee": username,
            },
        )

    def test_list_issues_http_failure(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("HTTP Error")
        mocker.patch("requests.get", return_value=mock_response)

        github_requests = GithubRequests(token="fake_token", repository_owner="owner", repository_name="repo")

        issues = github_requests.list_issues()

        assert issues is None

    def test_get_issue_returns_correct_details(self, mocker):
        mock_get = mocker.patch("requests.get")

        sample_response = {"id": 1, "title": "Sample Issue", "state": "open"}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response

        token = "valid_token"
        repository_owner = "owner_username"
        repository_name = "repository_name"
        username = "your_username"
        github_requests = GithubRequests(token, repository_owner, repository_name, username)

        issue = github_requests.get_issue(1)

        assert issue == sample_response

    def test_handle_http_request_failure_get_issue(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Mocked Request Exception")
        mocker.patch("requests.get", return_value=mock_response)

        github_requests = GithubRequests(token="fake_token", repository_owner="owner", repository_name="repo")

        issue = github_requests.get_issue(1)

        assert issue is None

    def test_change_issue_status(self, mocker):
        mock_response = mocker.Mock()
        mock_response.json.return_value = {"status": "closed"}
        mocker.patch("requests.patch", return_value=mock_response)

        github_requests = GithubRequests(token="fake_token", repository_owner="owner", repository_name="repo")

        response = github_requests.change_issue_status(issue_number=1, status="closed")

        assert response == {"status": "closed"}

    def test_commit_changes_successfully(self, mocker):
        mock_response_get = mocker.Mock()
        mock_response_get.status_code = 200
        mock_response_get.json.return_value = {
            "object": {"sha": "fake_sha"},
            "tree": {"sha": "fake_tree_sha"},
        }

        mocker.patch("requests.get", return_value=mock_response_get)

        mock_response_post_blob = mocker.Mock()
        mock_response_post_blob.json.return_value = {"sha": "fake_blob_sha"}
        mocker.patch(
            "requests.post",
            side_effect=[mock_response_post_blob, mock_response_post_blob],
        )

        mock_response_post_tree = mocker.Mock()
        mock_response_post_tree.json.return_value = {"sha": "fake_tree_sha"}
        mocker.patch(
            "requests.post",
            side_effect=[mock_response_post_tree, mock_response_post_tree],
        )

        mock_response_post_commit = mocker.Mock()
        mock_response_post_commit.json.return_value = {"sha": "fake_commit_sha"}
        mocker.patch("requests.post", return_value=mock_response_post_commit)

        mock_response_patch = mocker.Mock()
        mock_response_patch.json.return_value = {"sha": "fake_update_sha"}
        mocker.patch("requests.patch", return_value=mock_response_patch)

        github_requests = GithubRequests(token="fake_token", repository_owner="owner", repository_name="repo")

        result = github_requests.commit_changes(
            message="Commit message",
            branch_name="new_branch",
            files=[f"{os.path.dirname(os.path.realpath(__file__))}/test_github_requests.py"],
        )

        assert result == {"sha": "fake_update_sha"}

    def test_create_pull_request_default_parameters(self, mocker):
        mock_response = mocker.Mock()
        expected_json = {"id": 123, "title": "New Pull Request"}
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status.return_value = None
        mocker.patch("requests.post", return_value=mock_response)

        github_requests = GithubRequests(token="fake_token", repository_owner="owner", repository_name="repo")

        pull_request = github_requests.create_pull_request(head="feature_branch")

        assert pull_request == expected_json
