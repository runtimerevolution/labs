from unittest import skip
from unittest.mock import patch

import pytest
from core.models import Model, VectorizerModel
from embeddings.embedder import Embedder
from embeddings.ollama import OllamaEmbedder
from embeddings.openai import OpenAIEmbedder
from embeddings.vectorizers.vectorizer import Vectorizer
from llm.ollama import OllamaRequester
from llm.openai import OpenAIRequester
from tasks.checks import check_invalid_json
from tasks.llm import get_context, get_llm_response, get_prompt
from tests.constants import (
    OLLAMA_EMBEDDING_MODEL_NAME,
    OLLAMA_LLM_MODEL_NAME,
    OPENAI_EMBEDDING_MODEL_NAME,
    OPENAI_LLM_MODEL_NAME,
)


def call_llm_with_context(repository_path, issue_summary):
    if not issue_summary:
        raise ValueError("issue_summary cannot be empty.")

    embedder_class, *embeder_args = Model.get_active_embedding_model()
    embedder = Embedder(embedder_class, *embeder_args)

    vectorizer_class = VectorizerModel.get_active_vectorizer()
    Vectorizer(vectorizer_class, embedder).vectorize_to_database(None, repository_path)

    # find_similar_embeddings narrows down codebase to files that matter for the issue at hand.
    context = embedder.retrieve_embeddings(issue_summary, repository_path)

    prompt = get_prompt(issue_summary)
    prepared_context = get_context(context, prompt)

    return get_llm_response(prepared_context)


class TestCallLLMWithContext:
    def test_empty_summary(self):
        repository_path = "repository_path"
        issue_summary = ""

        with pytest.raises(Exception) as excinfo:
            call_llm_with_context(repository_path, issue_summary)

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
        is_invalid, message = check_invalid_json(llm_response)
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
        is_invalid, message = check_invalid_json(llm_response)
        assert is_invalid
        assert message == "Invalid JSON response."

    def test_invalid_json_structure(self):
        llm_response = {"choices": [{"message": {"content": '{"invalid_key": invalid_value"}'}}]}
        is_invalid, message = check_invalid_json(llm_response)
        assert is_invalid
        assert message == "Invalid JSON response."


class TestLocalLLM:
    @patch("embeddings.vectorizers.chunk_vectorizer.ChunkVectorizer.vectorize_to_database")
    @patch("embeddings.embedder.Embedder.retrieve_embeddings")
    @skip("This is used locally with an Ollama instance running in docker")
    def test_local_llm_connection(self, mocked_context, mocked_vectorize_to_database):
        mocked_context.return_value = [["file1", "/path/to/file1", "content"]]
        repository_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        success, response = call_llm_with_context(repository_destination, issue_summary)

        assert success

    @patch("llm.validate_llm_response")
    @patch("embeddings.vectorizers.base.Vectorizer.vectorize_to_database")
    @patch("llm.ollama.OllamaRequester.completion_without_proxy")
    @patch("embeddings.embedder.Embedder.retrieve_embeddings")
    @pytest.mark.django_db
    def test_local_llm_redirect(
        self,
        mocked_context,
        mocked_local_llm,
        mocked_vectorize_to_database,
        mocked_validate_llm_reponse,
        create_test_ollama_llm_config,
        create_test_ollama_embedding_config,
        create_test_chunk_vectorizer_config,
    ):
        mocked_context.return_value = [["file1", "/path/to/file1", "content"]]
        mocked_validate_llm_reponse.return_value = False, ""
        repository_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        call_llm_with_context(repository_destination, issue_summary)

        mocked_local_llm.assert_called_once()


class TestLLMRequester:
    @pytest.mark.django_db
    def test_openai_llm_requester(self, create_test_openai_llm_config):
        requester, model_name = Model.get_active_llm_model()

        assert issubclass(requester, OpenAIRequester)
        assert model_name == OPENAI_LLM_MODEL_NAME

    @pytest.mark.django_db
    def test_openai_embedder(self, create_test_openai_embedding_config):
        embedder, model_name = Model.get_active_embedding_model()

        assert issubclass(embedder, OpenAIEmbedder)
        assert model_name == OPENAI_EMBEDDING_MODEL_NAME

    @pytest.mark.django_db
    def test_ollama_llm_requester(self, create_test_ollama_llm_config):
        requester, model_name = Model.get_active_llm_model()

        assert issubclass(requester, OllamaRequester)
        assert model_name == OLLAMA_LLM_MODEL_NAME

    @pytest.mark.django_db
    def test_ollama_embedder(self, create_test_ollama_embedding_config):
        embedder, model_name = Model.get_active_embedding_model()

        assert issubclass(embedder, OllamaEmbedder)
        assert model_name == OLLAMA_EMBEDDING_MODEL_NAME
