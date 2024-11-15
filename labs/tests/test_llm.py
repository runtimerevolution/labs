import pytest
from llm import call_llm_with_context, check_invalid_json_response


class TestCallLlmWithContext:
    def test_empty_summary(self):
        issue_summary = ""
        repo_destination = "repo_destination"
        issue_summary = ""

        with pytest.raises(Exception) as excinfo:
            call_llm_with_context(repo_destination, issue_summary)

        assert "issue_summary cannot be empty" in str(excinfo.value)


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
