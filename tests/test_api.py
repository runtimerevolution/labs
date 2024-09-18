from unittest.mock import patch
from src.github.github import GithubRequests
from src.api.types import (
    CallLLMRequest,
    CodeMonkeyRequest,
    CommitChangesRequest,
    CreateBranchRequest,
    CreatePullRequest,
    GithubModel,
    IssueRequest,
    ListIssuesRequest,
)
from fastapi.testclient import TestClient
from src.api.main import app


class TestAPIClient:
    @patch("src.api.codemonkey_endpoints.call_llm_with_context")
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

    @patch("src.api.codemonkey_endpoints.run")
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

    @patch.object(GithubRequests, "list_issues")
    def test_successfull_list_issues(self, mocked_list):
        client = TestClient(app)
        request = GithubModel(
            github_token="valid_token", repo_owner="owner", repo_name="repo"
        )
        params = ListIssuesRequest()
        mocked_list.return_value = [
            {"id": 1, "title": "Issue 1", "state": "open"},
            {"id": 2, "title": "Issue 2", "state": "open"},
        ]

        response = client.post(
            "/github/list-issues",
            json={"request": request.__dict__, "params": params.__dict__},
        )

        assert response.status_code == 200
        assert response.json() == [
            {"id": 1, "title": "Issue 1", "state": "open"},
            {"id": 2, "title": "Issue 2", "state": "open"},
        ]

    @patch.object(GithubRequests, "get_issue")
    def test_successfull_get_issue(self, mocked_issue):
        client = TestClient(app)
        request = GithubModel(
            github_token="valid_token", repo_owner="owner", repo_name="repo"
        )
        params = IssueRequest(issue_number=1)
        mocked_issue.return_value = {"id": 1, "title": "Sample Issue", "state": "open"}

        response = client.post(
            "/github/get-issue",
            json={"request": request.__dict__, "params": params.__dict__},
        )

        assert response.status_code == 200
        assert response.json() == {"id": 1, "title": "Sample Issue", "state": "open"}

    @patch.object(GithubRequests, "create_branch")
    def test_successfull_create_branch(self, mocked_branch):
        client = TestClient(app)
        request = GithubModel(
            github_token="valid_token", repo_owner="owner", repo_name="repo"
        )
        params = CreateBranchRequest(branch_name="test_branch")
        mocked_branch.return_value = []

        response = client.post(
            "/github/create-branch",
            json={"request": request.__dict__, "params": params.__dict__},
        )

        assert response.status_code == 200
        assert response.json() == []

    @patch.object(GithubRequests, "commit_changes")
    def test_successfull_commit_changes(self, mocked_branch):
        client = TestClient(app)
        request = GithubModel(
            github_token="valid_token", repo_owner="owner", repo_name="repo"
        )
        params = CommitChangesRequest(
            branch_name="test_branch",
            message="Test message",
            files=["file1.py", "file2.py"],
        )
        mocked_branch.return_value = []

        response = client.post(
            "/github/commit-changes",
            json={"request": request.__dict__, "params": params.__dict__},
        )

        assert response.status_code == 200
        assert response.json() == []

    @patch.object(GithubRequests, "create_pull_request")
    def test_successfull_create_pull_request(self, mocked_branch):
        client = TestClient(app)
        request = GithubModel(
            github_token="valid_token", repo_owner="owner", repo_name="repo"
        )
        params = CreatePullRequest(head="test_branch")
        mocked_branch.return_value = []

        response = client.post(
            "/github/create-pull-request",
            json={"request": request.__dict__, "params": params.__dict__},
        )

        assert response.status_code == 200
        assert response.json() == []

    @patch.object(GithubRequests, "clone")
    def test_successfull_clone(self, mocked_branch):
        client = TestClient(app)
        request = GithubModel(
            github_token="valid_token", repo_owner="owner", repo_name="repo"
        )

        mocked_branch.return_value = []

        response = client.post(
            "/github/clone",
            json=request.__dict__,
        )

        assert response.status_code == 200
        assert response.json() == []

    @patch.object(GithubRequests, "clone")
    def test_wrong_input_format_clone(self, mocked_branch):
        client = TestClient(app)

        mocked_branch.return_value = []

        response = client.post(
            "/github/clone",
            json={"github_token": "valid_token", "repo_owner": "owner"},
        )

        assert response.status_code == 422
