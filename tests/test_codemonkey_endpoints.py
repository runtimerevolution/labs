from fastapi.testclient import TestClient
from unittest.mock import patch
from labs.api.main import app

client = TestClient(app)


class TestCodemonkeyEndpoints:
    @patch("labs.api.codemonkey_endpoints.run_on_local_repo_task")
    def test_run_on_local_repo_endpoint(self, mock_task):
        mock_task.return_value = None
        response = client.post(
            "/codemonkey/run_on_local_repo", json={"repo_path": "path/to/repo", "issue_text": "example issue text"}
        )
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.get_issue_task")
    def test_get_issue_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post(
            "/codemonkey/get_issue",
            json={
                "github_token": "token",
                "repo_owner": "owner",
                "repo_name": "name",
                "issue_number": 1,
                "username": "user",
            },
        )
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.run_on_repo_task")
    def test_run_on_repo_endpoint(self, mock_task):
        mock_task.return_value = None
        response = client.post(
            "/codemonkey/run_on_repo",
            json={
                "github_token": "token",
                "repo_owner": "owner",
                "repo_name": "name",
                "issue_number": 1,
                "username": "user",
                "original_branch": "main",
            },
        )
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.create_branch_task")
    def test_create_branch_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post(
            "/codemonkey/create_branch",
            json={
                "github_token": "token",
                "repo_owner": "owner",
                "repo_name": "name",
                "issue_number": 1,
                "username": "user",
                "original_branch": "main",
                "issue_title": "Title",
            },
        )
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.vectorize_repo_to_database_task")
    def test_vectorize_repo_to_database_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post("/codemonkey/vectorize_repo_to_database", json={"repo_destination": "destination/path"})
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.find_similar_embeddings_task")
    def test_find_similar_embeddings_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post("/codemonkey/find_similar_embeddings", json={"issue_body": "issue body"})
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.prepare_prompt_and_context_task")
    def test_prepare_prompt_and_context_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post("/codemonkey/prepare_prompt_and_context", json={"issue_body": "body", "embeddings": []})
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.get_llm_response_task")
    def test_get_llm_response_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post("/codemonkey/get_llm_response", json={"context": {}})
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.apply_code_changes_task")
    def test_apply_code_changes_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post("/codemonkey/apply_code_changes", json={"llm_response": "response"})
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.commit_changes_task")
    def test_commit_changes_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post(
            "/codemonkey/commit_changes",
            json={
                "github_token": "token",
                "repo_owner": "owner",
                "repo_name": "name",
                "username": "user",
                "branch_name": "branch",
                "files": [],
            },
        )
        assert response.status_code == 200
        mock_task.assert_called_once()

    @patch("labs.api.codemonkey_endpoints.create_pull_request_task")
    def test_create_pull_request_endpoint(self, mock_task):
        mock_task.return_value = {}
        response = client.post(
            "/codemonkey/create_pull_request",
            json={
                "github_token": "token",
                "repo_owner": "owner",
                "repo_name": "name",
                "username": "user",
                "branch_name": "branch",
                "original_branch": "main",
            },
        )
        assert response.status_code == 200
        mock_task.assert_called_once()
