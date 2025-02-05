import os

import openai
from litellm import completion


class OpenAIRequester:
    def __init__(self, model):
        self._model_name = model
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def completion_without_proxy(self, messages, *args, **kwargs):
        return self._model_name, completion(
            model=self._model_name,
            messages=messages,
            response_format={"type": "json_object"},
            *args,
            **kwargs,
        )
