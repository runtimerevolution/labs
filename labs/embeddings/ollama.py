from django.conf import settings
from embeddings.embedder import Embeddings
from ollama import Client

import logging

logger = logging.getLogger(__name__)

class OllamaEmbedder:
    def __init__(self, model):
        self._model_name = model
        self._client = Client(settings.LOCAL_LLM_HOST)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        logger.info("Embedding prompt of length=%d with Ollama model '%s'",
                    len(prompt), self._model_name)
        result = self._client.embed(self._model_name, prompt, *args, **kwargs)
        logger.info("Ollama returned embed result: %s", result)

        return Embeddings(
            model=result["model"],
            embeddings=result["embeddings"]
        )
