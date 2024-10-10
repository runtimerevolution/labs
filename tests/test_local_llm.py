from requests import patch

from labs.api.types import GithubModel
from labs.llm import call_llm_with_context


class TestLocalLLM:
    @patch("labs.middleware.vectorize_and_find_similar")
    def test_local_llm(self, mocked_context):
        mocked_context.return_value = [["file1", "/path/to/file1", "content1"]]
        github = GithubModel(github_token="token", repo_owner="owner", repo_name="repo")
        issue_summary = "Fix the bug in the authentication module"
        litellm_api_key = "fake_api_key"
        success, result = call_llm_with_context(github, issue_summary, litellm_api_key)
