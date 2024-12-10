import unittest
from unittest.mock import patch

from parsers.response_parser import modify_file


class TestModifyFile(unittest.TestCase):
    modify_file_args = {
        "path": "abc/test.txt",
        "content": ["content"],
        "line_number": 2,
    }

    @patch("parsers.response_parser.modify_line_in_file")
    def test_file_modified(self, mock_modify_line_in_file):
        file_path = modify_file(**self.modify_file_args)

        self.assertEqual(file_path, self.modify_file_args["path"])

    @patch("parsers.response_parser.modify_line_in_file")
    def test_error_handling(self, mock_modify_line_in_file):
        mock_modify_line_in_file.side_effect = Exception("error message")

        file_path = modify_file(**self.modify_file_args)

        self.assertEqual(file_path, None)
