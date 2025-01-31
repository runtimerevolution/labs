from django.conf import settings
from ollama import Client

import logging

logger = logging.getLogger(__name__)

class OllamaRequester:
    def __init__(self, model):
        self._model_name = model
        self._client = Client(settings.LOCAL_LLM_HOST)
        logger.info("OllamaRequester initialized with model '%s'", self._model_name)

    def completion_without_proxy(self, messages, *args, **kwargs):
        logger.info("Calling Ollama with messages=%s", messages)
        response = self._client.chat(model=self._model_name, messages=messages, format="json", *args, **kwargs)
        logger.info("Ollama response: %s", response)

        return self._model_name, {"choices": [response]}