import unittest
from unittest.mock import patch

import pytest
from core.models import Project, Prompt
from llm.context import CONTENT_TEMPLATE, get_context


@pytest.mark.usefixtures("create_test_project")
class TestGetContext(unittest.TestCase):
    test_prompt_content = "test prompt"
    test_prompt = {"role": "user", "content": test_prompt_content}

    test_file_paths = ["file_path"]
    test_file_contents = "some_text"
    test_files_context = {
        "role": "system",
        "content": CONTENT_TEMPLATE.format(file=test_file_paths[0], content=test_file_contents, mimetype="plaintext"),
    }

    @staticmethod
    def get_persona_context(project_id):
        return {"role": "system", "content": Prompt.get_persona(project_id)}

    @patch("llm.context.get_file_content", return_value=test_file_contents)
    @pytest.mark.django_db
    def test_empty_file_paths(self, mocked_get_file_contents):
        project = Project.objects.first()
        context = get_context(files_path=[], prompt=self.test_prompt_content, project_id=project.id)

        expected_context = [self.test_prompt, self.get_persona_context(project.id)]

        self.assertEqual(len(context), len(expected_context))
        for c in context:
            self.assertIn(c, expected_context)

    @patch("llm.context.get_file_content", return_value=test_file_contents)
    @pytest.mark.django_db
    def test_success(self, mocked_get_file_contents):
        project = Project.objects.first()
        context = get_context(files_path=self.test_file_paths, prompt=self.test_prompt_content, project_id=project.id)

        expected_context = [self.test_files_context, self.test_prompt, self.get_persona_context(project.id)]

        self.assertEqual(len(context), len(expected_context))
        for c in context:
            self.assertIn(c, expected_context)
