from ollama import Client

from labs.config.configuration_variables import LOCAL_LLM_HOST
from labs.embeddings.base import Embedder, Embeddings


class OllamaEmbedder(Embedder):
    def __init__(self, model):
        self._model = model

        self._client = Client(LOCAL_LLM_HOST)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        result = self._client.embed(self._model, prompt, *args, **kwargs)
        return Embeddings(model=result["model"], embeddings=result["embeddings"])
