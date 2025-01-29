# llm/gemini.py

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
          

    def completion_without_proxy(self, messages: List[Dict[str, str]], *args, **kwargs):
        """
        messages expected to be in the following format:
        [
            {
                "role": "user",
                "content": ""
            }
        ]
        Where role can be "user", "assistant", "system".
        And content is the body of the message.
        """
        prompt = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages])
        response = self.generative_model.generate_content(prompt)
        return self._model_name, response.text

