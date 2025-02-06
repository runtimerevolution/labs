import os
import google.generativeai as genai
from embeddings.embedder import Embeddings

class GeminiEmbedder:
    def __init__(self, model: str):
        self._model_name = model
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
            if isinstance(emb, list) and len(emb) > 0 and isinstance(emb[0], list):
                flat_vector = emb[0]
            else:
                flat_vector = emb
            
            return Embeddings(
                model=self._model_name,
                model_config=result.get("model_config", {}),
                embeddings=[flat_vector]
            )

        except Exception as e:
            raise ValueError(f"Error embedding with Gemini: {e}") from e
