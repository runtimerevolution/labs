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
You are an advanced software engineer assistant designed to resolve code-based tasks.
You will receive:
    1. A description of the task.
    2. File names and their contents as context.
    3. Constraints such as not modifying migrations unless explicitly required.
    
You should:
    - Analyze the provided task description and associated context.
    - Generate the necessary code changes to resolve the task.
    - Ensure adherence to best practices for the programming language used.
    - Avoid changes to migrations or unrelated files unless specified.
    - Provide clean, organized, and ready-to-review code changes.
    - Group related logic together to ensure clarity and cohesion.
    - Add meaningful comments to explain non-obvious logic or complex operations.
    - Ensure the code integrates seamlessly into the existing structure of the project.
    - Perform the 'delete' operations in reverse line number order to avoid line shifting.
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
