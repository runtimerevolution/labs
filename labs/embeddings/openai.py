import os

import openai
from embeddings.embedder import Embedder, Embeddings
from litellm import embedding


class OpenAIEmbedder:
    def __init__(self, model):
        self._model_name = model

        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        result = embedding(model=self._model_name, input=prompt, *args, **kwargs)
        return Embeddings(
            model=result.model,
            model_config=result.model_config,
            embeddings=[data["embedding"] for data in result.data],
        )
