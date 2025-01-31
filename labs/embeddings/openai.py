import os
import openai
from embeddings.embedder import Embeddings
from litellm import embedding

import logging

logger = logging.getLogger(__name__)

class OpenAIEmbedder:
    def __init__(self, model):
        self._model_name = model
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        logger.info("Embedding prompt of length=%d with model '%s'",
                    len(prompt), self._model_name)
        result = embedding(model=self._model_name, input=prompt, *args, **kwargs)

        logger.info("OpenAI returned embedding data: %s", result.data)

        return Embeddings(
            model=result.model,
            model_config=result.model_config,
            embeddings=[data["embedding"] for data in result.data],
        )
