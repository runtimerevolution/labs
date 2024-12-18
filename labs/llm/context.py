from typing import List

from file_handler import get_file_contents

CONTENT_TEMPLATE = "File: {file}\nContent:\n{content}"


def get_context(files_path: List[str], prompt: str):
    context = []
    for path in files_path:
        content = get_file_contents(path)
        context.append(dict(role="system", content=CONTENT_TEMPLATE.format(file=path, content=content)))

    context.append(dict(role="user", content=prompt))
    return context
