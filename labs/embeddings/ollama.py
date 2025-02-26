from django.conf import settings
from embeddings.embedder import Embeddings
from ollama import Client
from core.models import Model


class OllamaEmbedder:
    def __init__(self, model: Model):
        self._model_name = model.model_name
        self._client = Client(settings.LOCAL_LLM_HOST)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        result = self._client.embed(self._model_name, prompt, *args, **kwargs)
        return Embeddings(model=result["model"], embeddings=result["embeddings"])
