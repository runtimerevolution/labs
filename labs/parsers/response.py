import json
import logging
from typing import List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Step(BaseModel):
    type: str
    path: str
    content: str
    line: Optional[int] = None


class Response(BaseModel):
    steps: List[Step]


def parse_llm_output(text_output) -> Response:
    return Response.model_validate_json(text_output)


def create_file(path: str, content: str) -> str | None:
    logger.debug(f"Creating file on path: {path}")
    try:
        with open(path, "w") as file:
            file.write(content)
        logger.debug(f"File created at {path}")
        return path
    except Exception as e:
        logger.error(f"Error creating file at {path}: {e}")
        return None


def modify_file(path: str, content: str, line_number: int) -> str | None:
    logger.debug(f"Modifying file on path: {path}")
    try:
        with open(path, "w") as file:
            file.write("\n" + content)
        logger.debug(f"File modified at {path}")
        return path
    except Exception as e:
        logger.error(f"Error modifying file at {path}: {e}")
        return None


def is_valid_json(text):
    try:
        json.loads(text)
    except ValueError:
        return False
    return True
