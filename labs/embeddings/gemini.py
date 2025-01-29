import os
import google.generativeai as genai
from embeddings.embedder import Embeddings

class GeminiEmbedder:
    def __init__(self, model: str):
        self._model_name = model

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        genai.configure(api_key=api_key)
        

    def embed(self, prompt: str, *args, **kwargs) -> Embeddings:
        try:
            result = genai.embed_content(
                model=self._model_name,
                content=prompt,
                *args, 
                **kwargs,
            )
            
            embedding = result.get('embedding')
            if not embedding:
                raise ValueError("No embedding found in Gemini response.")
            
            return Embeddings(
                model=self._model_name,
                model_config=result.get("model_config", {}),
                embeddings=[{'embedding': embedding}],
            )
        
        except Exception as e:
            raise ValueError(f"Error embedding with Gemini: {e}") from e
