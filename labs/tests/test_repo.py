import unittest
from typing import List
from unittest.mock import patch

from parsers.response_parser import CreateStep, ModifyStep, PullRequest
from repo import call_agent_to_apply_code_changes


class TestCallAgentToApplyCodeChanges(unittest.TestCase):
    example_no_step: List[CreateStep | ModifyStep] = []
    example_single_step: List[CreateStep | ModifyStep] = [
        ModifyStep(type="modify", path="/path/to/modify/file", content="file content", line_number=1)
    ]
    example_multiple_steps: List[CreateStep | ModifyStep] = [
        CreateStep(type="create", path="/path/to/create/file", content="file content"),
        ModifyStep(type="modify", path="/path/to/modify/file", content="file content", line_number=1),
    ]

    @patch("repo.modify_file", return_value="/path/to/modify/file")
    @patch("repo.parse_llm_output", return_value=PullRequest(steps=example_single_step))
    def test_single_file(self, mock_parse_llm_output, mock_modify_file):
        file_paths = call_agent_to_apply_code_changes("")
        self.assertCountEqual(file_paths, [step.path for step in self.example_single_step])

    @patch("repo.modify_file", return_value="/path/to/modify/file")
    @patch("repo.create_file", return_value="/path/to/create/file")
    @patch("repo.parse_llm_output", return_value=PullRequest(steps=example_multiple_steps))
    def test_multiple_files(self, mock_parse_llm_output, mock_create_file, mock_modify_file):
        file_paths = call_agent_to_apply_code_changes("")
        self.assertCountEqual(file_paths, [step.path for step in self.example_multiple_steps])

    @patch("repo.parse_llm_output", return_value=PullRequest(steps=example_no_step))
    def test_no_files(self, mock_parse_llm_output):
        file_paths = call_agent_to_apply_code_changes("")
        self.assertListEqual(file_paths, [])
