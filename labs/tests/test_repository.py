from typing import List
from unittest.mock import patch

from django.test import TestCase
from parsers.response import Response, Step
from tasks.repository import apply_code_changes


class TestApplyCodeChanges(TestCase):
    NO_STEP: List[Step] = []
    SINGLE_STEP: List[Step] = [Step(type="modify", path="/path/to/modify/file", content="file content", line=1)]
    MULTIPLE_STEP: List[Step] = [
        Step(type="create", path="/path/to/create/file", content="file content"),
        Step(type="modify", path="/path/to/modify/file", content="file content", line=1),
    ]

    @patch("file_handler.modify_file_line")
    @patch("tasks.repository.parse_llm_output", return_value=Response(steps=SINGLE_STEP))
    def test_single_file(self, mock_parse_llm_output, mock_modify_file_line):
        file_paths = apply_code_changes("")
        self.assertCountEqual(file_paths, [step.path for step in self.SINGLE_STEP])

    @patch("file_handler.modify_file_line")
    @patch("file_handler.create_file")
    @patch("tasks.repository.parse_llm_output", return_value=Response(steps=MULTIPLE_STEP))
    def test_multiple_files(self, mock_parse_llm_output, mock_create_file, mock_modify_file_line):
        file_paths = apply_code_changes("")
        self.assertCountEqual(file_paths, [step.path for step in self.MULTIPLE_STEP])

    @patch("tasks.repository.parse_llm_output", return_value=Response(steps=NO_STEP))
    def test_no_files(self, mock_parse_llm_output):
        file_paths = apply_code_changes("")
        self.assertListEqual(file_paths, [])
