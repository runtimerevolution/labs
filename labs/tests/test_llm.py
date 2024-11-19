from unittest import skip
from unittest.mock import patch

import conftest
import pytest
from core.models import Config
from embeddings.ollama import OllamaEmbedder
from embeddings.openai import OpenAIEmbedder
from litellm_service.ollama import OllamaRequester
from litellm_service.openai import OpenAIRequester
from llm import call_llm_with_context, check_invalid_json_response


class TestCallLLMWithContext:
    def test_empty_summary(self):
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


class TestLocalLLM:
    @patch("embeddings.vectorizers.chunk_vectorizer.ChunkVectorizer.vectorize_to_database")
    @patch("embeddings.base.Embedder.retrieve_embeddings")
    @skip("This is used locally with an Ollama instance running in docker")
    def test_local_llm_connection(self, mocked_context, mocked_vectorize_to_database):
        mocked_context.return_value = [["file1", "/path/to/file1", "content"]]
        repo_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        success, response = call_llm_with_context(repo_destination, issue_summary)

        assert success

    @patch("llm.validate_llm_response")
    @patch("embeddings.vectorizers.chunk_vectorizer.ChunkVectorizer.vectorize_to_database")
    @patch("litellm_service.ollama.OllamaRequester.completion_without_proxy")
    @patch("embeddings.base.Embedder.retrieve_embeddings")
    @pytest.mark.django_db
    def test_local_llm_redirect(
        self,
        mocked_context,
        mocked_local_llm,
        mocked_vectorize_to_database,
        mocked_validate_llm_reponse,
        create_test_ollama_llm_config,
        create_test_ollama_embedding_config,
    ):
        mocked_context.return_value = [["file1", "/path/to/file1", "content"]]
        mocked_validate_llm_reponse.return_value = False, ""
        repo_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        call_llm_with_context(repo_destination, issue_summary)

        mocked_local_llm.assert_called_once()


class TestLLMRequester:
    @pytest.mark.django_db
    def test_openai_llm_requester(self, create_test_openai_llm_config):
        requester, model_name = Config.get_active_llm_model()

        assert issubclass(requester, OpenAIRequester)
        assert model_name == conftest.OPENAI_LLM_MODEL_NAME

    @pytest.mark.django_db
    def test_openai_embedder(self, create_test_openai_embedding_config):
        embedder, model_name = Config.get_active_embedding_model()

        assert issubclass(embedder, OpenAIEmbedder)
        assert model_name == conftest.OPENAI_EMBEDDING_MODEL_NAME

    @pytest.mark.django_db
    def test_ollama_llm_requester(self, create_test_ollama_llm_config):
        requester, model_name = Config.get_active_llm_model()

        assert issubclass(requester, OllamaRequester)
        assert model_name == conftest.OLLAMA_LLM_MODEL_NAME

    @pytest.mark.django_db
    def test_ollama_embedder(self, create_test_ollama_embedding_config):
        embedder, model_name = Config.get_active_embedding_model()

        assert issubclass(embedder, OllamaEmbedder)
        assert model_name == conftest.OLLAMA_EMBEDDING_MODEL_NAME
