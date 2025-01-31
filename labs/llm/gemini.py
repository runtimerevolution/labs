import os
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
        logger.info("Calling Gemini with messages=%s", messages)
        prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages])
        logger.info("Gemini message to promp: %s", prompt)
        response = self.generative_model.generate_content(prompt)
        logger.info("Gemini response: %s", response)

        return self._model_name, response.text
