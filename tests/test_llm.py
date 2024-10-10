from unittest.mock import patch
import pytest

from labs.api.types import GithubModel
from labs.litellm_service.request import RequestLiteLLM
from labs.llm import call_llm_with_context, check_invalid_json_response


class TestCallLlmWithContext:
    # Successfully calls the LLM with the provided context and returns the expected output
    @patch("labs.database.embeddings")
    @patch.object(RequestLiteLLM, "completion_without_proxy")
    @patch("labs.repo.call_agent_to_apply_code_changes")
    def test_successful_llm_call_with_context(self, mocked_agent, mocked_completion, mocked_embeddings):
        # Mocking dependencies
        mocked_embeddings.return_value = [["file1", "/path/to/file1", "content1"]]
        mocked_completion.return_value = (
            "model",
            {
                "choices": [
                    {
                        "message": {
                            "content": '{"steps": [{"type": "create", "path": "/path/to/file", "content": "file content"}]}'
                        }
                    }
                ]
            },
        )
        mocked_agent.return_value = ["file1"]

        issue_summary = "Fix the bug in the authentication module"
        repo_destination = "."

        success, result = call_llm_with_context(repo_destination, issue_summary)

        assert success
        assert result == (
            "model",
            {
                "choices": [
                    {
                        "message": {
                            "content": '{"steps": [{"type": "create", "path": "/path/to/file", "content": "file content"}]}'
                        }
                    }
                ]
            },
        )

    # Ensure the GithubModel is instantiated correctly with the correct parameters

    def test_empty_summary(self):
        issue_summary = ""
        repo_destination = "repo_destination"
        issue_summary = ""

        with pytest.raises(Exception) as excinfo:
            call_llm_with_context(repo_destination, issue_summary)

        assert "issue_summary cannot be empty" in str(excinfo.value)
        # Corrects the mocking of find_similar_embeddings attribute in the rag module


class TestCheckInvalidJsonResponse:
    def test_valid_json_response(self):
        llm_response = {
            "choices": [
                {
                    "message": {
                        "content": '{"steps": [{"type": "create", "path": "/path/to/file", "content": "file content"}]}'
                    }
                }
            ]
        }
        is_invalid, message = check_invalid_json_response(llm_response)
        print (is_invalid, message)
        assert not is_invalid
        assert message == ""

    def test_invalid_json_response(self):
        llm_response = {
            "choices": [
                {
                    "message": {
                        "content": '{"steps": [{"type": "create", "path": "/path/to/file", "content": "file content"'
                    }
                }
            ]
        }
        is_invalid, message = check_invalid_json_response(llm_response)
        assert is_invalid
        assert message == "Invalid JSON response."

    def test_invalid_json_structure(self):
        llm_response = {"choices": [{"message": {"content": '{"invalid_key": \invalid_value"}'}}]}
        is_invalid, message = check_invalid_json_response(llm_response)
        assert is_invalid
        assert message == "Invalid JSON response."
