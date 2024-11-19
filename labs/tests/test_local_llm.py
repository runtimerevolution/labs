from unittest import skip
from unittest.mock import patch

import pytest
from llm import call_llm_with_context


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
        create_test_llm_config,
        create_test_embedding_config,
    ):
        mocked_context.return_value = [["file1", "/path/to/file1", "content"]]
        mocked_validate_llm_reponse.return_value = False, ""
        repo_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        call_llm_with_context(repo_destination, issue_summary)

        mocked_local_llm.assert_called_once()
