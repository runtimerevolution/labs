import logging
import mimetypes
from typing import List

from core.models import Prompt
from file_handler import get_file_content

logger = logging.getLogger(__name__)

MIMETYPE_MD_NAME = {
    "text/plain": "plaintext",
    "application/json": "json",
    "text/html": "html",
    "text/x-python": "python",
}

CONTENT_TEMPLATE = "The following is the code in `{file}`:\n\n```{mimetype}\n{content}\n```"


def get_file_mimetype(file_path: str) -> str:
    if not file_path:
        raise ValueError("File path cannot be empty")

    mimetype, _ = mimetypes.guess_type(file_path)
    try:
        return MIMETYPE_MD_NAME[mimetype]

    except KeyError:
        return MIMETYPE_MD_NAME["text/plain"]


def get_context(files_path: List[str], prompt: str):
    context = [dict(role="system", content=Prompt.get_persona())]

    for file in files_path:
        content = get_file_content(file)
        mimetype = get_file_mimetype(file)
        context.append(
            dict(role="system", content=CONTENT_TEMPLATE.format(file=file, mimetype=mimetype, content=content))
        )

    context.append(dict(role="user", content=prompt))
    return context
