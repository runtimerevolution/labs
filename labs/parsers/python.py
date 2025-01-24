import ast
import os


class PythonFileParser(ast.NodeVisitor):
    """Parse a Python file and return its structure."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.imports = []
        self.classes = []
        self.functions = []
        self.constants = []
        self.main_block = False
        self.global_statements = []
        self.comments = []

    def _create_func_dict(self, func_node):
        return {
            "name": func_node.name,
            "start_line": func_node.lineno - 1,
            "end_line": func_node.end_lineno,
            "parameters": [arg.arg for arg in func_node.args.args],
            "returns": self._get_return_type(func_node.returns),
        }

    def _get_return_type(self, return_value):
        if not return_value:
            return "None"

        elif isinstance(return_value, ast.Constant):
            return type(return_value.value).__name__

        elif isinstance(return_value, ast.Name):
            return return_value.id

        elif isinstance(return_value, ast.BinOp):
            return [
                self._get_return_type(return_value.left),
                self._get_return_type(return_value.right),
            ]

        elif isinstance(return_value, ast.List):
            return "list"

        elif isinstance(return_value, ast.Dict):
            return "dict"

        elif isinstance(return_value, ast.Tuple):
            return "tuple"

        elif isinstance(return_value, ast.Lambda):
            return "lambda"

        else:
            return "unknown"

    def visit_Import(self, node):
        self.imports.append(
            {
                "module": node.names[0].name,
                "alias": None,
                "start_line": node.lineno - 1,
                "end_line": node.end_lineno,
            }
        )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.imports.append(
            {
                "module": node.module,
                "alias": node.names[0].name,
                "start_line": node.lineno - 1,
                "end_line": node.end_lineno,
            }
        )
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        tmp_class = {
            "name": node.name,
            "start_line": node.lineno - 1,
            "end_line": node.end_lineno,
            "methods": [],
        }
        for func in node.body:
            if isinstance(func, ast.FunctionDef):
                method_dict = self._create_func_dict(func)
                tmp_class["methods"].append(method_dict)
                func.is_method = True
        self.classes.append(tmp_class)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if not hasattr(node, "is_method"):
            self.functions.append(self._create_func_dict(node))
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            value = self._simplify_value(node.value)
            const_dict = {
                "name": node.targets[0].id,
                "start_line": node.lineno - 1,
                "end_line": node.end_lineno,
            }
            if value is not None:
                const_dict["value"] = value
            self.constants.append(const_dict)
        self.generic_visit(node)

    def visit_If(self, node):
        if (
            isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == "__name__"
            and any(isinstance(op, ast.Eq) for op in node.test.ops)
            and any(isinstance(cmp, ast.Str) and cmp.s == "__main__" for cmp in node.test.comparators)
        ):
            self.main_block = True
        self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            self.comments.append(
                {
                    "type": "docstring",
                    "content": node.value.s,
                    "start_line": node.lineno - 1,
                    "end_line": node.end_lineno,
                }
            )
        self.generic_visit(node)

    def visit(self, node):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            self.comments.append(
                {
                    "type": "docstring",
                    "content": node.value.s,
                    "start_line": node.lineno - 1,
                    "end_line": node.end_lineno,
                }
            )
        else:
            super().visit(node)

    def visit_Module(self, node):
        for n in node.body:
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Str):
                self.comments.append(
                    {
                        "type": "docstring",
                        "content": n.value.s,
                        "start_line": n.lineno - 1,
                        "end_line": n.end_lineno,
                    }
                )
            else:
                self.visit(n)

    def visit_Global(self, node):
        self.global_statements.append(
            {
                "type": "global",
                "identifiers": node.names,
                "start_line": node.lineno - 1,
                "end_line": node.end_lineno,
            }
        )
        self.generic_visit(node)

    def get_structure(self):
        return {
            "file_name": self.file_name,
            "imports": self.imports,
            "classes": self.classes,
            "functions": self.functions,
            "constants": self.constants,
            "main_block": self.main_block,
            "global_statements": self.global_statements,
            "comments": self.comments,
        }

    def _simplify_value(self, value):
        if isinstance(value, (ast.Str, ast.Num, ast.Constant)):  # Python 3.8+ uses ast.Constant
            return value.value if hasattr(value, "value") else value.n
        elif isinstance(value, ast.NameConstant):
            return value.value
        return None


def parse_python_file(file_path: str) -> str | dict:
    """
    Parses a specified Python file and returns its structure.
    Args:
        file_path (str): Path to the Python file.
    Returns:
        str | dict: A structure representation of the file, or an error message if the file is not found or is a directory.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    elif os.path.isdir(file_path):
        raise IsADirectoryError(f"{file_path} is a directory")

    with open(file_path, "r") as source:
        file_content = source.read()

    parser = PythonFileParser(file_name=file_path)
    tree = ast.parse(file_content, file_path)
    parser.visit(tree)

    return parser.get_structure()


def get_lines_code(file_path: str, start_line: int, end_line: int) -> str:
    """
    Retrieves and returns a range of lines from a specified file.
    Args:
        file_path (str): Path to the file.
        start_line (int): The starting line number (0-based index).
        end_line (int): The ending line number (exclusive).
    Returns:
        str: The specified lines joined as a string, or an error message if the file is not found or is a directory.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    elif os.path.isdir(file_path):
        raise IsADirectoryError(f"{file_path} is a directory")

    with open(file_path, "r") as f:
        lines = f.readlines()
    return "\n".join(map(lambda s: s.strip(), lines[start_line:end_line]))
