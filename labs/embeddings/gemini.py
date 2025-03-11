import os

from embeddings.embedder import Embeddings
from google import genai


class GeminiEmbedder:
    def __init__(self, model):
        self._model_name = model.name
        api_key = os.environ.get("GEMINI_API_KEY")
        self._client = genai.Client(api_key=api_key)

    def embed(self, prompt: str, *args, **kwargs) -> Embeddings:
        try:
            result = self._client.models.embed_content(
                model=self._model_name,
                contents=[prompt],
                *args,
                **kwargs,
            )

            assert result.embeddings

            embeddings = []

            for content_embedding in result.embeddings:
                if content_embedding.values:
                    embeddings.append(content_embedding.values)

            return Embeddings(
                model=self._model_name,
                model_config=result.model_config,
                embeddings=embeddings,
                tokens=None,
            )

        except Exception as e:
            raise ValueError(f"Error embedding with Gemini: {e}") from e
