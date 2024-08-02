from unittest.mock import patch
from labs.api.types import CallLLMRequest, CodeMonkeyRequest, GithubModel
from fastapi.testclient import TestClient
from labs.api.main import app


class TestAPIClient:
    @patch("labs.api.codemonkey_endpoints.call_llm_with_context")
    def test_successfull_call_llm_with_context(self, mocked_call):
        client = TestClient(app)
        github = GithubModel(
            github_token="valid_token", repo_owner="owner", repo_name="repo"
        )
        params = CallLLMRequest(issue_summary="This is a test issue", token="token")

        mocked_call.return_value = ["file1.py", "file2.py"]

        response = client.post(
            "/codemonkey/llm_with_context",
            json={"github": github.__dict__, "params": params.__dict__},
        )

        assert response.status_code == 200
        assert response.json() == ["file1.py", "file2.py"]

    @patch("labs.api.codemonkey_endpoints.run")
    def test_successfull_call_run(self, mocked_call):
        client = TestClient(app)
        request = CodeMonkeyRequest(
            github_token="valid_token",
            repo_owner="owner",
            repo_name="repo",
            litellm_api_key="token",
            issue_number=1,
        )

        mocked_call.return_value = None

        response = client.post(
            "/codemonkey/run",
            json=request.__dict__,
        )

        assert response.status_code == 200
