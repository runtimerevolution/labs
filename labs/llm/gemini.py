import os
import json
import re
from typing import List, Dict, Tuple, Any

import google.generativeai as genai

class GeminiRequester:
    def __init__(self, model: str):
        self._model_name = model
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.generative_model = genai.GenerativeModel(self._model_name)

    def completion_without_proxy(self, messages: List[Dict[str, str]], *args, **kwargs) -> Tuple[str, Dict[str, Any]]:
        prompt_string = json.dumps(messages)
        try:
            response = self.generative_model.generate_content(contents=prompt_string, *args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}") from e

        response_text = response.text
        match = re.search(r"```json\n(.*)\n```", response_text, re.DOTALL)
        if not match:
            raise ValueError("Could not find JSON block in Gemini response.")

        json_string = match.group(1)
        try:
            json_response = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in Gemini response: {e}") from e

        gemini_response = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(json_response)
                    }
                }
            ]
        }

        return self._model_name, gemini_response