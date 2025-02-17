import os
from tempfile import NamedTemporaryFile
from unittest import TestCase

from file_handler import create_file, delete_file_line, get_file_content, modify_file_line


class TestFileHandler(TestCase):
    TEMPORARY_CONTENT = """
    Line 1
    Line 2
    Line 4
    """
    NEW_CONTENT = "    Line 3\n"
    # Insert variables
    INSERT_LINE = 3
    INSERT_LINE_EXPECTED_CONTENT = """
    Line 1
    Line 2
    Line 3
    Line 4
    """
    INSERT_EOF_LINE = 6
    INSERT_EOF_EXPECTED_CONTENT = """
    Line 1
    Line 2
    Line 4
    
    Line 3
"""
    # Overwrite variables
    OVERWRITE_LINE = 4
    OVERWRITE_LINE_EXPECTED_CONTENT = """
    Line 1
    Line 2
    Line 3
    """
    OVERWRITE_EOF_LINE = 6
    OVERWRITE_EOF_EXPECTED_CONTENT = """
    Line 1
    Line 2
    Line 4
    """
    # Delete variables
    DELETE_LINE = 4
    DELETE_LINE_EXPECTED_CONTENT = """
    Line 1
    Line 2
    """

    def assertFileContentEqual(self, file_path, expected_content):
        with open(file_path, "r") as file_handler:
            self.assertEqual(expected_content, file_handler.read())

    def setUp(self):
        self.temporary_file = NamedTemporaryFile(mode="w+", delete=False)
        self.temporary_file.write(self.TEMPORARY_CONTENT)
        self.temporary_file.flush()
        self.temporary_file.close()

    def test_get_file_content(self):
        content = get_file_content(self.temporary_file.name)
        self.assertEqual(content, self.TEMPORARY_CONTENT)

    def test_create_file(self):
        # Remove the existing file created in setUp
        try:
            os.remove(self.temporary_file.name)

        except FileNotFoundError:
            pass

        create_file(self.temporary_file.name, self.TEMPORARY_CONTENT)
        self.assertFileContentEqual(self.temporary_file.name, self.TEMPORARY_CONTENT)

    def test_insert_file_line(self):
        modify_file_line(self.temporary_file.name, self.NEW_CONTENT, self.INSERT_LINE)
        self.assertFileContentEqual(self.temporary_file.name, self.INSERT_LINE_EXPECTED_CONTENT)

    def test_insert_end_of_file(self):
        modify_file_line(self.temporary_file.name, self.NEW_CONTENT, self.INSERT_EOF_LINE)
        self.assertFileContentEqual(self.temporary_file.name, self.INSERT_EOF_EXPECTED_CONTENT)

    def test_overwrite_file_line(self):
        modify_file_line(self.temporary_file.name, self.NEW_CONTENT, self.OVERWRITE_LINE, overwrite=True)
        self.assertFileContentEqual(self.temporary_file.name, self.OVERWRITE_LINE_EXPECTED_CONTENT)

    def test_overwrite_end_of_file(self):
        modify_file_line(self.temporary_file.name, self.NEW_CONTENT, self.OVERWRITE_EOF_LINE, overwrite=True)
        self.assertFileContentEqual(self.temporary_file.name, self.OVERWRITE_EOF_EXPECTED_CONTENT)

    def test_delete_file_line(self):
        delete_file_line(self.temporary_file.name, self.DELETE_LINE)
        self.assertFileContentEqual(self.temporary_file.name, self.DELETE_LINE_EXPECTED_CONTENT)

    def tearDown(self):
        os.remove(self.temporary_file.name)
