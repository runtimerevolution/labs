from unittest.mock import patch

from core.models import Project
from django.test import TestCase
from llm.context import CONTENT_TEMPLATE, get_context
from tests.constants import FILE_CONTENT, PERSONA, PROMPT
from tests.utilities import create_test_config


class TestContext(TestCase):
    FILE_PATH = "/file/path"
    RAW_PROMPT = dict(role="user", content=PROMPT)
    RAW_PERSONA_CONTEXT = dict(role="system", content=PERSONA)
    RAW_FILES_CONTEXT = dict(
        role="system", content=CONTENT_TEMPLATE.format(file=FILE_PATH, content=FILE_CONTENT, mimetype="plaintext")
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_config()

        cls.project = Project.objects.create(name="test", path="/test/path")

    @patch("core.models.Prompt.get_persona", return_value=PERSONA)
    @patch("llm.context.get_file_content", return_value=FILE_CONTENT)
    def test_empty_file_paths(self, mocked_get_file_content, mocked_get_persona):
        expected_context = [self.RAW_PROMPT, self.RAW_PERSONA_CONTEXT]

        context = get_context(files_path=[], prompt=PROMPT, project_id=self.project.id)
        self.assertEqual(len(context), len(expected_context))
        for elem in context:
            self.assertIn(elem, expected_context)

    @patch("core.models.Prompt.get_persona", return_value=PERSONA)
    @patch("llm.context.get_file_content", return_value=FILE_CONTENT)
    def test_file_paths(self, mocked_get_file_content, mocked_get_persona):
        expected_context = [self.RAW_FILES_CONTEXT, self.RAW_PROMPT, self.RAW_PERSONA_CONTEXT]

        context = get_context(files_path=[self.FILE_PATH], prompt=PROMPT, project_id=self.project.id)
        self.assertEqual(len(context), len(expected_context))
        for elem in context:
            self.assertIn(elem, expected_context)
