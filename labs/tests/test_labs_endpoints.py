from unittest.mock import patch

from api.codemonkey_endpoints import router
from core.models import Project
from django.test import TestCase
from ninja.testing import TestAsyncClient
from tests.utilities import create_test_config

client = TestAsyncClient(router)


class TestLabsEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_config()

        cls.project = Project.objects.create(name="test", path="/test/path")

    @patch("api.codemonkey_endpoints.run_on_local_repository_task")
    async def test_run_on_local_repository_endpoint(self, mock_task):
        response = await client.post(
            "/run_on_local_repository",
            json={"project_id": self.project.id, "prompt": "test issue text"},
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.get_issue_task", return_value={})
    async def test_get_issue_endpoint(self, mock_task):
        response = await client.post(
            "/get_issue",
            json={
                "token": "token",
                "repository_owner": "owner",
                "repository_name": "name",
                "issue_number": 1,
                "username": "user",
            },
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.run_on_repository_task")
    async def test_run_on_repository_endpoint(self, mock_task):
        response = await client.post(
            "/run_on_repository",
            json={
                "token": "token",
                "repository_owner": "owner",
                "repository_name": "name",
                "issue_number": 1,
                "username": "user",
                "original_branch": "main",
            },
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.create_branch_task", return_value={})
    async def test_create_branch_endpoint(self, mock_task):
        response = await client.post(
            "/create_branch",
            json={
                "token": "token",
                "repository_owner": "owner",
                "repository_name": "name",
                "issue_number": 1,
                "username": "user",
                "original_branch": "main",
                "issue_title": "Title",
            },
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.vectorize_repository_task", return_value={})
    async def test_vectorize_repository_endpoint(self, mock_task):
        response = await client.post(
            "/vectorize_repository",
            json={"project_id": self.project.id},
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.find_embeddings_task", return_value={})
    async def test_find_embeddings_endpoint(self, mock_task):
        response = await client.post("/find_embeddings", json={"project_id": self.project.id, "prompt": "issue body"})
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.prepare_prompt_and_context_task", return_value={})
    async def test_prepare_prompt_and_context_endpoint(self, mock_task):
        response = await client.post(
            "/prepare_prompt_and_context",
            json={"project_id": self.project.id, "prompt": "body", "embeddings": []},
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.get_llm_response_task", return_value={})
    async def test_get_llm_response_endpoint(self, mock_task):
        response = await client.post("/get_llm_response", json={"context": {}})
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.apply_code_changes_task", return_value={})
    async def test_apply_code_changes_endpoint(self, mock_task):
        response = await client.post("/apply_code_changes", json={"changes": "response"})
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.commit_changes_task", return_value={})
    async def test_commit_changes_endpoint(self, mock_task):
        response = await client.post(
            "/commit_changes",
            json={
                "token": "token",
                "repository_owner": "owner",
                "repository_name": "name",
                "username": "user",
                "branch_name": "branch",
                "files": [],
            },
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()

    @patch("api.codemonkey_endpoints.create_pull_request_task", return_value={})
    async def test_create_pull_request_endpoint(self, mock_task):
        response = await client.post(
            "/create_pull_request",
            json={
                "token": "token",
                "repository_owner": "owner",
                "repository_name": "name",
                "username": "user",
                "changes_branch_name": "branch",
                "base_branch_name": "main",
            },
        )
        self.assertEqual(response.status_code, 200)
        mock_task.assert_called_once()
