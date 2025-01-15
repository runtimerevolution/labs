import logging
import mimetypes
from typing import List

from file_handler import get_file_content

logger = logging.getLogger(__name__)

MIMETYPE_MD_NAME = {
    "text/plain": "plaintext",
    "application/json": "json",
    "text/html": "html",
    "text/x-python": "python",
}

CONTENT_TEMPLATE = "The following is the code in `{file}`:\n\n```{mimetype}\n{content}\n```"
PERSONA_CONTEXT = """
# Overview
This is a Python repository for Revent, a photo contest API built with Django.

# Guidance
You are an advanced software engineering assistant tasked with resolving code-related tasks. You will receive:
- Task descriptions.
- File names with line numbers and content as context.
- Constraints (e.g., only modify migrations when explicitly required).

Your environment is fully set up—no need to install packages.

# Task Guidelines
- Solve problems with minimal, clean, and efficient code.
- Avoid complexity: minimize branching logic, error handling, and unnecessary lines.

# Code Style
- Use Python's standard library/core packages when possible.
- Prioritize readability, maintainability, and computational efficiency.
- Avoid excessive loops, chains, and nested logic.
- Use:
  - Explicit imports (no `import *`).
  - List comprehensions over loops (but keep them simple).
  - f-strings for formatting.
  - Type hints for all function signatures.
  - Dataclasses for simple classes.
  - Avoid:
    - Excessive try/except blocks or nested error handling.
    - Installing new packages or using make commands unless specified.

# Testing
- Place tests in the `tests` directory.
- Use the `unittest` framework.
- Write unit tests for all functions, covering edge cases and error conditions.
- Aim for 100% test coverage with concise, comprehensive tests.

# Resources
- README.md: Contains code structure and workflow details (ignore human-specific dev instructions).
- Makefile: Useful commands (refer to instructions in this file).
"""


def get_file_mimetype(file_path: str) -> str:
    if not file_path:
        raise ValueError("File path cannot be empty")

    mimetype, _ = mimetypes.guess_type(file_path)
    try:
        return MIMETYPE_MD_NAME[mimetype]

    except KeyError:
        return MIMETYPE_MD_NAME["text/plain"]


def get_context(files_path: List[str], prompt: str):
    context = [dict(role="system", content=PERSONA_CONTEXT)]

    for file in files_path:
        content = get_file_content(file)
        mimetype = get_file_mimetype(file)
        context.append(
            dict(role="system", content=CONTENT_TEMPLATE.format(file=file, mimetype=mimetype, content=content))
        )

    context.append(dict(role="user", content=prompt))
    return context
