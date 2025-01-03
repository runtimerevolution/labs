import unittest
from unittest.mock import patch

from file_handler import modify_file_line


class TestModifyFile(unittest.TestCase):
    modify_file_args = {
        "file_path": "abc/test.txt",
        "content": ["content"],
        "line_number": 2,
    }

    @patch("file_handler.modify_file_line")
    def test_file_modified(self, mock_modify_file_line):
        modify_file_line(**self.modify_file_args)

    @patch("file_handler.modify_file_line")
    def test_error_handling(self, mock_modify_file_line):
        mock_modify_file_line.side_effect = Exception("error message")

        modify_file_line(**self.modify_file_args)
