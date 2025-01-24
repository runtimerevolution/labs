from unittest import TestCase, skip
from unittest.mock import patch

import pytest
from core.models import Model, VectorizerModel
from embeddings.embedder import Embedder
from embeddings.ollama import OllamaEmbedder
from embeddings.openai import OpenAIEmbedder
from embeddings.vectorizers.vectorizer import Vectorizer
from llm.checks import ValidationError, check_invalid_json
from llm.context import CONTENT_TEMPLATE, get_context
from llm.ollama import OllamaRequester
from llm.openai import OpenAIRequester
from llm.prompt import get_prompt
from tasks.llm import get_llm_response
from tests.constants import (
    OLLAMA_EMBEDDING_MODEL_NAME,
    OLLAMA_LLM_MODEL_NAME,
    OPENAI_EMBEDDING_MODEL_NAME,
    OPENAI_LLM_MODEL_NAME,
)


def call_llm_with_context(repository_path, issue_summary, project):
    if not issue_summary:
        raise ValueError("issue_summary cannot be empty.")

    embedder_class, *embeder_args = Model.get_active_embedding_model()
    embedder = Embedder(embedder_class, *embeder_args)

    vectorizer_class = VectorizerModel.get_active_vectorizer(project)
    Vectorizer(vectorizer_class, embedder).vectorize_to_database(None, repository_path)

    # find_similar_embeddings narrows down codebase to files that matter for the issue at hand.
    file_paths = embedder.retrieve_files_path(issue_summary, repository_path)

    prompt = get_prompt(issue_summary)
    prepared_context = get_context(file_paths, prompt)

    return get_llm_response(prepared_context)


class TestCallLLMWithContext:
    @pytest.mark.django_db
    def test_empty_summary(self, create_test_project):
        repository_path = "repository_path"
        issue_summary = ""

        with pytest.raises(Exception) as excinfo:
            call_llm_with_context(repository_path, issue_summary, project=create_test_project)

        assert "issue_summary cannot be empty" in str(excinfo.value)


class TestCheckInvalidJsonResponse(TestCase):
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

        check_invalid_json(llm_response)

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

        with self.assertRaises(ValidationError, msg="Malformed JSON LLM response."):
            check_invalid_json(llm_response)

    def test_invalid_json_structure(self):
        llm_response = {"choices": [{"message": {"content": '{"invalid_key": "invalid_value"}'}}]}

        with self.assertRaises(ValidationError, msg="JSON response from LLM not match the expected format."):
            check_invalid_json(llm_response)


class TestLocalLLM:
    test_file_paths = ["file_path"]
    test_file_contents = "some_text"
    test_context = {
        "role": "system",
        "content": CONTENT_TEMPLATE.format(file=test_file_paths[0], content=test_file_contents, mimetype="text/plain"),
    }

    @patch("file_handler.get_file_content", return_value="test file contents")
    @patch("embeddings.vectorizers.chunk_vectorizer.ChunkVectorizer.vectorize_to_database")
    @patch("embeddings.embedder.Embedder.retrieve_files_path")
    @skip("This is used locally with an Ollama instance running in docker")
    @pytest.mark.django_db
    def test_local_llm_connection(
        self, mocked_retrieve_files_path, mocked_vectorize_to_database, mocked_get_file_content, create_test_project
    ):
        mocked_retrieve_files_path.return_value = ["/path/to/file1"]
        repository_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        success, response = call_llm_with_context(repository_destination, issue_summary, create_test_project)

        assert success

    @patch("llm.context.get_file_content", return_value="test file contents")
    @patch("tasks.llm.run_response_checks")
    @patch("embeddings.vectorizers.vectorizer.Vectorizer.vectorize_to_database")
    @patch("llm.ollama.OllamaRequester.completion_without_proxy")
    @patch("embeddings.embedder.Embedder.retrieve_files_path")
    @pytest.mark.django_db
    def test_local_llm_redirect(
        self,
        mocked_retrieve_files_path,
        mocked_completion_without_proxy,
        mocked_vectorize_to_database,
        mocked_run_response_checks,
        mocked_get_file_content,
        create_test_ollama_llm_config,
        create_test_ollama_embedding_config,
        create_test_chunk_vectorizer_config,
        create_test_project,
    ):
        mocked_retrieve_files_path.return_value = ["/path/to/file1"]
        mocked_run_response_checks.return_value = False, ""
        repository_path = "repo"
        issue_summary = "Fix the bug in the authentication module"
        call_llm_with_context(repository_path, issue_summary, create_test_project)

        mocked_completion_without_proxy.assert_called_once()


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
