import os
import json
import re
import google.generativeai as genai
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class GeminiRequester:
    def __init__(self, model: str):
        self._model_name = model
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.generative_model = genai.GenerativeModel(self._model_name)
        logger.info("GeminiRequester initialized with model '%s'", self._model_name)

    def completion_without_proxy(self, messages: List[Dict[str, str]], *args, **kwargs):
        try:
            prompt_string = json.dumps(messages)
            response = self.generative_model.generate_content(contents=prompt_string, *args, **kwargs)

            response_text = response.text
            match = re.search(r"```json\n(.*)\n```", response_text, re.DOTALL)
            if match:
                json_string = match.group(1)
                try:
                    json_response = json.loads(json_string)

                    gemini_response = {
                        "choices": [
                            {
                                "message": {
                                    "content": json.dumps(json_response),
                                    "finish_reason": None
                                }
                            }
                        ]
                    }

                    return self._model_name, gemini_response

                except json.JSONDecodeError:
                    logger.error("Extracted JSON is still invalid.")
                    return self._model_name, None

            else:
                logger.error("Could not find JSON block in Gemini response.")
                return self._model_name, None

        except Exception as e:
            logger.error(f"Gemini completion error: {e}")
            return self._model_name, None