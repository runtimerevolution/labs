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
