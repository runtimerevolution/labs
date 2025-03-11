import os

import openai
from embeddings.embedder import Embeddings
from litellm import embedding


class OpenAIEmbedder:
    def __init__(self, model):
        self._model_name = model.name
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        result = embedding(model=self._model_name, input=prompt, *args, **kwargs)

        assert result.model is not None
        assert result.usage is not None

        return Embeddings(
            model=result.model,
            model_config=result.model_config,
            embeddings=[data["embedding"] for data in result.data],
            tokens=result.usage.total_tokens,
        )
