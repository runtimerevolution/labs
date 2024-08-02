from unittest.mock import patch
import pytest
from middleman_functions import call_llm_with_context
from labs.api.types import GithubModel
from litellm_service.request import RequestLiteLLM


class TestCallLlmWithContext:

    # Successfully calls the LLM with the provided context and returns the expected output
    @patch("middleman_functions.find_similar_embeddings")
    @patch.object(RequestLiteLLM, "completion_without_proxy")
    @patch("middleman_functions.vectorize_to_db")
    @patch("middleman_functions.call_agent_to_apply_code_changes")
    def test_successful_llm_call_with_context(
        self, mocked_agent, mocked_vectorized, mocked_completion, mocked_embeddings
    ):

        # Mocking dependencies
        mocked_embeddings.return_value = [["file1", "/path/to/file1", "content1"]]
        mocked_completion.return_value = (
            "model",
            {"choices": [{"message": {"content": "response"}}]},
        )
        mocked_agent.return_value = ["file1"]

        github = GithubModel(github_token="token", repo_owner="owner", repo_name="repo")
        issue_summary = "Fix the bug in the authentication module"
        litellm_api_key = "fake_api_key"

        result = call_llm_with_context(github, issue_summary, litellm_api_key)

        assert result == ["file1"]

    # Ensure the GithubModel is instantiated correctly with the correct parameters

    def test_empty_summary(self, mocker):
        # Mocking dependencies
        mocker.patch("vector.vectorize_to_db")
        github = GithubModel(github_token="token", repo_owner="owner", repo_name="repo")
        issue_summary = ""
        litellm_api_key = "fake_api_key"

        with pytest.raises(Exception) as excinfo:
            call_llm_with_context(github, issue_summary, litellm_api_key)

        assert "issue_summary cannot be empty" in str(excinfo.value)
        # Corrects the mocking of find_similar_embeddings attribute in the rag module

    @patch("middleman_functions.find_similar_embeddings")
    def test_corrected_find_similar_embeddings_direct_instantiation(
        self, mocked_embeddings, mocker
    ):

        # Mocking dependencies
        mocked_embeddings.return_value = [["file1", "/path/to/file1", "content1"]]
        mocker.patch("vector.vectorize_to_db")
        mocker.patch.object(
            RequestLiteLLM,
            "completion_without_proxy",
            side_effect=Exception("Error message"),
        )

        github = GithubModel(github_token="token", repo_owner="owner", repo_name="repo")
        issue_summary = "Fix the bug in the authentication module"
        litellm_api_key = "fake_api_key"

        with pytest.raises(Exception) as exc_info:
            call_llm_with_context(github, issue_summary, litellm_api_key)

        assert str(exc_info.value) == "Error calling LLM: Error message"
