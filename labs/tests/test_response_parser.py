import unittest
from unittest.mock import patch

from parsers.response import modify_file


class TestModifyFile(unittest.TestCase):
    modify_file_args = {
        "path": "abc/test.txt",
        "content": ["content"],
        "line": 2,
    }

    @patch("parsers.response.modify_file_line")
    def test_file_modified(self, mock_modify_file_line):
        file_path = modify_file(**self.modify_file_args)

        self.assertEqual(file_path, self.modify_file_args["path"])

    @patch("parsers.response.modify_file_line")
    def test_error_handling(self, mock_modify_file_line):
        mock_modify_file_line.side_effect = Exception("error message")

        file_path = modify_file(**self.modify_file_args)

        self.assertEqual(file_path, None)
