import unittest
from unittest.mock import patch

from llm.context import CONTENT_TEMPLATE, PERSONA_CONTEXT, get_context


class TestGetContext(unittest.TestCase):
    test_prompt_content = "test prompt"
    test_prompt = {"role": "user", "content": test_prompt_content}

    test_file_paths = ["file_path"]
    test_file_contents = "some_text"
    test_files_context = {
        "role": "system",
        "content": CONTENT_TEMPLATE.format(file=test_file_paths[0], content=test_file_contents, mimetype="plaintext"),
    }

    test_persona_context = {
        "role": "system",
        "content": PERSONA_CONTEXT,
    }

    @patch("llm.context.get_file_content", return_value=test_file_contents)
    def test_empty_file_paths(self, mocked_get_file_contents):
        context = get_context(files_path=[], prompt=self.test_prompt_content)

        expected_context = [self.test_prompt, self.test_persona_context]

        self.assertEqual(len(context), len(expected_context))
        for c in context:
            self.assertIn(c, expected_context)

    @patch("llm.context.get_file_content", return_value=test_file_contents)
    def test_success(self, mocked_get_file_contents):
        context = get_context(files_path=self.test_file_paths, prompt=self.test_prompt_content)

        expected_context = [self.test_files_context, self.test_prompt, self.test_persona_context]

        self.assertEqual(len(context), len(expected_context))
        for c in context:
            self.assertIn(c, expected_context)
