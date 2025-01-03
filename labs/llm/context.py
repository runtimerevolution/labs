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
CONTENT_TEMPLATE = "The following is the Python code in `{file}`:\n\n````{mimetype}\n{content}\n```"


def get_file_mimetype(file_path: str) -> str:
    if not file_path:
        return ""

    mimetype, _ = mimetypes.guess_type(file_path)
    try:
        return MIMETYPE_MD_NAME[mimetype]

    except KeyError:
        return MIMETYPE_MD_NAME["text/plain"]


def get_context(files_path: List[str], prompt: str):
    context = []
    for path in files_path:
        mimetype = get_file_mimetype(path)
        content = get_file_content(path)
        context.append(
            dict(role="system", content=CONTENT_TEMPLATE.format(file=path, mimetype=mimetype, content=content))
        )

    context.append(dict(role="user", content=prompt))
    return context
