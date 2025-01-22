import ast
from tempfile import NamedTemporaryFile

from django.test import TestCase
from parsers.python import PythonFileParser, get_lines_code, parse_python_file

TEST_CODE = """
import os
        
def sum_function(a: int, b: int) -> int:
    return a + b
            
class DummyClass:
    def return_hi(self):
        return "Hi"
"""


class TestPythonFileParser(TestCase):
    def setUp(self):
        self.test_code = TEST_CODE
        self.parser = PythonFileParser("file.py")
        self.tree = ast.parse(self.test_code)
        self.parser.visit(self.tree)

    def test__create_func_dict(self):
        func_node = next(node for node in self.tree.body if isinstance(node, ast.FunctionDef))
        func_dict = self.parser._create_func_dict(func_node)

        self.assertEqual(func_dict["name"], "sum_function")
        self.assertEqual(func_dict["parameters"], ["a", "b"])
        self.assertEqual(func_dict["returns"], "int")

    def test__get_return_type(self):
        self.assertEqual(self.parser._get_return_type(ast.Constant(value=100)), "int")
        self.assertEqual(self.parser._get_return_type(ast.Constant(value="value")), "str")
        self.assertEqual(self.parser._get_return_type(ast.List(elts=[])), "list")
        self.assertEqual(
            self.parser._get_return_type(ast.Dict(keys=[1, 2, 3], values=["a", "b", "c"])),
            "dict",
        )
        self.assertEqual(self.parser._get_return_type(ast.Tuple(elts=["a", "b", "c"])), "tuple")

    def test_get_lines_code(self):
        with NamedTemporaryFile("w+") as temporary_python_file:
            temporary_python_file.write(TEST_CODE)
            temporary_python_file.seek(0)

            result = get_lines_code(temporary_python_file.name, 3, 5)
            self.assertEqual(
                result,
                "\n".join([line.strip() for line in TEST_CODE.splitlines()][3:5]),
            )

    def test_get_lines_code_file_not_exist(self):
        self.assertRaises(FileNotFoundError, get_lines_code, "file_not_exist.py", 3, 5)

    def test_get_line_code_is_directory(self):
        self.assertRaises(IsADirectoryError, get_lines_code, "/tmp", 3, 5)

    def test_parse_python_file(self):
        with NamedTemporaryFile("w+") as temporary_python_file:
            temporary_python_file.write(TEST_CODE)
            temporary_python_file.seek(0)

            result = parse_python_file(temporary_python_file.name)

            self.assertEqual(result["file_name"], temporary_python_file.name)
            self.assertEqual(
                result["imports"],
                [{"module": "os", "alias": None, "start_line": 1, "end_line": 2}],
            )
            self.assertEqual(
                result["classes"],
                [
                    {
                        "name": "DummyClass",
                        "start_line": 6,
                        "end_line": 9,
                        "methods": [
                            {
                                "name": "return_hi",
                                "start_line": 7,
                                "end_line": 9,
                                "parameters": ["self"],
                                "returns": "None",
                            }
                        ],
                    }
                ],
            )
            self.assertEqual(
                result["functions"],
                [
                    {
                        "name": "sum_function",
                        "start_line": 3,
                        "end_line": 5,
                        "parameters": ["a", "b"],
                        "returns": "int",
                    }
                ],
            )
            self.assertEqual(result["constants"], [])
            self.assertEqual(result["global_statements"], [])
            self.assertEqual(result["comments"], [])
            self.assertFalse(result["main_block"])

    def test_parse_python_file_file_not_exist(self):
        self.assertRaises(FileNotFoundError, parse_python_file, "file_not_exist.py")

    def test_parse_python_file_is_directory(self):
        self.assertRaises(IsADirectoryError, parse_python_file, "/tmp")
