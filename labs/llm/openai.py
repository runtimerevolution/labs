import logging
import os
from typing import Any, Dict, Tuple

import openai
from litellm import completion
from litellm.types.utils import ModelResponse

logger = logging.getLogger(__name__)


class OpenAIRequester:
    def __init__(self, model):
        self._model_name = model.name
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def completion_without_proxy(self, messages, *args, **kwargs) -> Tuple[str, Dict[str, Any], int]:
        response: ModelResponse = completion(
            model=self._model_name,
            messages=messages,
            response_format={"type": "json_object"},
            *args,
            **kwargs,
        )

        tokens: int = response["usage"]["total_tokens"]

        return self._model_name, response, tokens
