import json
import os
from typing import Any, Dict, List, Tuple

from google import genai
from google.genai import types


class GeminiRequester:
    def __init__(self, model):
        self._model_name = model.name
        api_key = os.environ.get("GEMINI_API_KEY")
        self._client = genai.Client(api_key=api_key)

    def completion_without_proxy(
        self,
        messages: List[Dict[str, str]],
        *args,
        **kwargs,
    ) -> Tuple[str, Dict[str, Any]]:
        try:
            gemini_response = self._client.models.generate_content(
                model=self._model_name,
                contents=json.dumps(messages),
                config=types.GenerateContentConfig(response_mime_type="application/json"),
                *args,
                **kwargs,
            )

            return self._model_name, {"choices": [{"message": {"content": gemini_response.text}}]}
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}") from e
