import unittest
from typing import List
from unittest.mock import patch

from parsers.response import Response, Step
from tasks.repository import apply_code_changes


class TestApplyCodeChanges(unittest.TestCase):
    example_no_step: List[Step] = []
    example_single_step: List[Step] = [Step(type="modify", path="/path/to/modify/file", content="file content", line=1)]
    example_multiple_steps: List[Step] = [
        Step(type="create", path="/path/to/create/file", content="file content"),
        Step(type="modify", path="/path/to/modify/file", content="file content", line=1),
    ]

    @patch("tasks.repository.modify_file", return_value="/path/to/modify/file")
    @patch("tasks.repository.parse_llm_output", return_value=Response(steps=example_single_step))
    def test_single_file(self, mock_parse_llm_output, mock_modify_file):
        file_paths = apply_code_changes("")
        self.assertCountEqual(file_paths, [step.path for step in self.example_single_step])

    @patch("tasks.repository.modify_file", return_value="/path/to/modify/file")
    @patch("tasks.repository.create_file", return_value="/path/to/create/file")
    @patch("tasks.repository.parse_llm_output", return_value=Response(steps=example_multiple_steps))
    def test_multiple_files(self, mock_parse_llm_output, mock_create_file, mock_modify_file):
        file_paths = apply_code_changes("")
        self.assertCountEqual(file_paths, [step.path for step in self.example_multiple_steps])

    @patch("tasks.repository.parse_llm_output", return_value=Response(steps=example_no_step))
    def test_no_files(self, mock_parse_llm_output):
        file_paths = apply_code_changes("")
        self.assertListEqual(file_paths, [])
