from unittest import skip
from unittest.mock import patch

from core.models import Model, ModelTypeEnum, Project, ProviderEnum, VectorizerModel
from django.test import TestCase
from embeddings.embedder import Embedder
from embeddings.ollama import OllamaEmbedder
from embeddings.openai import OpenAIEmbedder
from embeddings.vectorizers.vectorizer import Vectorizer
from llm.checks import ValidationError, check_invalid_json
from llm.context import get_context
from llm.ollama import OllamaRequester
from llm.openai import OpenAIRequester
from llm.prompt import get_prompt
from tasks.llm import get_llm_response
from tests.constants import (
    FILE_CONTENT,
    INSTRUCTION,
    OLLAMA_EMBEDDING_MODEL_NAME,
    OLLAMA_LLM_MODEL_NAME,
    OPENAI_EMBEDDING_MODEL_NAME,
    OPENAI_LLM_MODEL_NAME,
    PERSONA,
)
from tests.utilities import create_test_config


def call_llm_with_context(project, issue_summary):
    embedder_class, *embeder_args = Model.get_active_embedding_model()
    embedder = Embedder(embedder_class, *embeder_args)

    vectorizer_class = VectorizerModel.get_active_vectorizer(project)
    Vectorizer(vectorizer_class, embedder).vectorize_to_database(None, project)

    file_paths = embedder.retrieve_files_path(issue_summary, project)

    prompt = get_prompt(project.id, issue_summary)
    prepared_context = get_context(project.id, file_paths, prompt)

    return get_llm_response(prepared_context)


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


class TestLocalLLM(TestCase):
    def setUp(self):
        super().setUpClass()
        create_test_config()

        self.project = Project.objects.create(name="test", path="/test/path")

    @patch("core.models.Prompt.get_persona", return_value=PERSONA)
    @patch("core.models.Prompt.get_instruction", return_value=INSTRUCTION)
    @patch("llm.context.get_file_content", return_value=FILE_CONTENT)
    @patch("tasks.llm.run_response_checks")
    @patch("embeddings.vectorizers.vectorizer.Vectorizer.vectorize_to_database")
    @patch("llm.ollama.OllamaRequester.completion_without_proxy")
    @patch("embeddings.embedder.Embedder.retrieve_files_path")
    def test_local_llm_redirect(
        self,
        mocked_retrieve_files_path,
        mocked_completion_without_proxy,
        mocked_vectorize_to_database,
        mocked_run_response_checks,
        mocked_get_file_content,
        mocked_get_instruction,
        mocked_get_persona,
    ):
        Model.objects.create(
            model_type=ModelTypeEnum.LLM.name,
            provider=ProviderEnum.OLLAMA.name,
            model_name=OLLAMA_LLM_MODEL_NAME,
            active=True,
        )
        Model.objects.create(
            model_type=ModelTypeEnum.EMBEDDING.name,
            provider=ProviderEnum.OLLAMA.name,
            model_name=OLLAMA_EMBEDDING_MODEL_NAME,
            active=True,
        )

        mocked_retrieve_files_path.return_value = ["/path/to/file1"]
        mocked_run_response_checks.return_value = False, ""

        issue_summary = "Fix the bug in the authentication module"
        call_llm_with_context(self.project, issue_summary)

        mocked_completion_without_proxy.assert_called_once()

    @patch("llm.context.get_file_content", return_value=FILE_CONTENT)
    @patch("embeddings.vectorizers.chunk_vectorizer.ChunkVectorizer.vectorize_to_database")
    @patch("embeddings.embedder.Embedder.retrieve_files_path")
    @skip("This is used locally with an Ollama instance running in docker")
    def test_local_llm_connection(
        self, mocked_retrieve_files_path, mocked_vectorize_to_database, mocked_get_file_content
    ):
        # Creates the required configuration objects
        Model.objects.create(
            model_type=ModelTypeEnum.LLM.name,
            provider=ProviderEnum.OLLAMA.name,
            model_name=OLLAMA_LLM_MODEL_NAME,
            active=True,
        )
        Model.objects.create(
            model_type=ModelTypeEnum.EMBEDDING.name,
            provider=ProviderEnum.OLLAMA.name,
            model_name=OLLAMA_EMBEDDING_MODEL_NAME,
            active=True,
        )

        mocked_retrieve_files_path.return_value = ["/path/to/file1"]
        issue_summary = "Fix the bug in the authentication module"
        success, response = call_llm_with_context(self.project, issue_summary)

        self.assertTrue(success)


class TestLLMRequesterOllama(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_config()

        Model.objects.create(
            model_type=ModelTypeEnum.LLM.name,
            provider=ProviderEnum.OLLAMA.name,
            model_name=OLLAMA_LLM_MODEL_NAME,
            active=True,
        )
        Model.objects.create(
            model_type=ModelTypeEnum.EMBEDDING.name,
            provider=ProviderEnum.OLLAMA.name,
            model_name=OLLAMA_EMBEDDING_MODEL_NAME,
            active=True,
        )

    def test_ollama_llm_requester(self):
        requester, model_name = Model.get_active_llm_model()

        assert issubclass(requester, OllamaRequester)
        self.assertEqual(model_name, OLLAMA_LLM_MODEL_NAME)

    def test_ollama_embedder(self):
        embedder, model_name = Model.get_active_embedding_model()

        assert issubclass(embedder, OllamaEmbedder)
        self.assertEqual(model_name, OLLAMA_EMBEDDING_MODEL_NAME)


class TestLLMRequestOpenAI(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_config()

        Model.objects.create(
            model_type=ModelTypeEnum.LLM.name,
            provider=ProviderEnum.OPENAI.name,
            model_name=OPENAI_LLM_MODEL_NAME,
            active=True,
        )
        Model.objects.create(
            model_type=ModelTypeEnum.EMBEDDING.name,
            provider=ProviderEnum.OPENAI.name,
            model_name=OPENAI_EMBEDDING_MODEL_NAME,
            active=True,
        )

    def test_openai_llm_requester(self):
        requester, model_name = Model.get_active_llm_model()

        assert issubclass(requester, OpenAIRequester)
        self.assertEqual(model_name, OPENAI_LLM_MODEL_NAME)

    def test_openai_embedder(self):
        embedder, model_name = Model.get_active_embedding_model()

        assert issubclass(embedder, OpenAIEmbedder)
        self.assertEqual(model_name, OPENAI_EMBEDDING_MODEL_NAME)
