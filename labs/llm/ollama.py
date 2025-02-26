from django.conf import settings
from typing import Tuple, Dict, Any
from ollama import Client


class OllamaRequester:
    def __init__(self, model):
        self._model_name = model.name
        self._model_max_output_tokens = model.max_output_tokens
        self._client = Client(settings.LOCAL_LLM_HOST)

    def completion_without_proxy(self, messages, *args, **kwargs) -> Tuple[str, Dict[str, Any]]:
        response = self._client.chat(
            model=self._model_name,
            messages=messages,
            format="json",
            options={"num_ctx": self._model_max_output_tokens},
            *args,
            **kwargs,
        )
        return self._model_name, {"choices": [response]}
