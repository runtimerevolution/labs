import os
import google.generativeai as genai
from embeddings.embedder import Embeddings
from core.models import Model

class GeminiEmbedder:
    def __init__(self, model: Model):
        self._model_name = model.model_name
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

    def embed(self, prompt: str, *args, **kwargs) -> Embeddings:
        try:
            result = genai.embed_content(
                model=self._model_name,
                content=prompt,
                *args, 
                **kwargs,
            )

            emb = result.get("embedding")
            if isinstance(emb, list) and all(isinstance(e, list) for e in emb):
                flat_vectors = emb
            else:
                flat_vectors = [emb]
    
            return Embeddings(
                model=self._model_name,
                model_config=result.get("model_config", {}),
                embeddings=flat_vectors
            )

        except Exception as e:
            raise ValueError(f"Error embedding with Gemini: {e}") from e
