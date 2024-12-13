from typing import List

from file_handling import get_file_contents

CONTENT_TEMPLATE = "File: {file}, Content: {content}"


def get_context(file_paths: List[str], prompt: str):
    context = []
    for file in file_paths:
        content = get_file_contents(file)
        context.append(dict(role="system", content=CONTENT_TEMPLATE.format(file=file, content=content)))

    context.append(dict(role="user", content=prompt))
    return context
