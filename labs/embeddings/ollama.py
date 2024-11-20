from config.configuration_variables import LOCAL_LLM_HOST
from embeddings.embedder import Embedder, Embeddings
from ollama import Client


class OllamaEmbedder:
    def __init__(self, model):
        self._model_name = model

        self._client = Client(LOCAL_LLM_HOST)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        result = self._client.embed(self._model_name, prompt, *args, **kwargs)
        return Embeddings(model=result["model"], embeddings=result["embeddings"])
