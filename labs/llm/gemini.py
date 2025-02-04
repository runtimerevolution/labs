import os
import json
from typing import List, Dict, Tuple, Any

import google.generativeai as genai

class GeminiRequester:
    def __init__(self, model: str):
        self._model_name = model
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.generative_model = genai.GenerativeModel(
            self._model_name, 
            generation_config={"response_mime_type": "application/json"}
        )

    def completion_without_proxy(
        self,
        messages: List[Dict[str, str]],
        *args,
        **kwargs,
    ) -> Tuple[str, Dict[str, Any]]:

        try:
            response = self.generative_model.generate_content(
                contents=json.dumps(messages),
                *args,
                **kwargs,
            )

            try:
                json_response = json.loads(response.text)
                return self._model_name, {
                    "choices": [{"message": {"content": json.dumps(json_response)}}]
                }
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid Gemini JSON response: {e}, Raw response: {getattr(response, 'text', 'No response text')}"
                ) from e

        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}") from e