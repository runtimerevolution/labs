from unittest.mock import patch

from labs.llm import call_llm_with_context


class TestLocalLLM:
    @patch("labs.llm.vectorize_to_database")
    @patch("labs.llm.find_similar_embeddings")
    def test_local_llm(self, mocked_context, mocked_vectorize_to_database):
        mocked_context.return_value = [["ficheiro1", "/path/to/ficheiro1", "conteudo"]]
        repo_destination = "repo"
        issue_summary = "Fix the bug in the authentication module"
        success, response = call_llm_with_context(repo_destination, issue_summary)

        assert success
