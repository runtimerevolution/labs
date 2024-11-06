from unittest import skip
from unittest.mock import patch

from labs.llm import call_llm_with_context


class TestLocalLLM:
    @patch("labs.database.vectorize.chunk_vectorizer.ChunkVectorizer.vectorize_to_database")
    @patch("labs.llm.find_similar_embeddings")
    @patch("labs.llm.settings.LOCAL_LLM", True)
    @skip("This is used locally with an Ollama instance running in docker")
    def test_local_llm_connection(self, mocked_context, mocked_vectorize_to_database):
        mocked_context.return_value = [["file1", "/path/to/file1", "content"]]
        repo_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        success, response = call_llm_with_context(repo_destination, issue_summary)

        assert success

    @patch("labs.database.vectorize.chunk_vectorizer.ChunkVectorizer.vectorize_to_database")
    @patch("labs.llm.RequestLiteLLM")
    @patch("labs.llm.RequestLocalLLM")
    @patch("labs.llm.find_similar_embeddings")
    @patch("labs.llm.settings.LOCAL_LLM", True)
    def test_local_llm_redirect(self, mocked_context, mocked_local_llm, mocked_llm, mocked_vectorize_to_database):
        mocked_context.return_value = [["file1", "/path/to/file1", "content"]]
        repo_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        call_llm_with_context(repo_destination, issue_summary)

        mocked_local_llm.assert_called_once()
        mocked_llm.assert_not_called()
