import os
import json
from typing import List, Dict, Tuple, Any

import google.generativeai as genai


class GeminiRequester:
    def __init__(self, model: str):
        self._model_name = model
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.generative_model = genai.GenerativeModel(self._model_name)

    def completion_without_proxy(
        self,
        messages: List[Dict[str, str]],
        *args,
        **kwargs,
    ) -> Tuple[str, Dict[str, Any]]:

        generation_config = genai.GenerationConfig(response_mime_type="application/json")

        try:
            gemini_response = self.generative_model.generate_content(
                contents=json.dumps(messages),
                generation_config=generation_config,
                *args,
                **kwargs,
            )

            return self._model_name, {
                "choices": [{"message": {"content": gemini_response.text}}]
            }

        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}") from e
