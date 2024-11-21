import os

import openai
from litellm import completion


class OpenAIRequester:
    def __init__(self, model):
        self._model_name = model

        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def completion_without_proxy(self, messages, *args, **kwargs):
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
        return self._model_name, completion(
            model=self._model_name,
            messages=messages,
            response_format={"type": "json_object"},
            *args,
            **kwargs,
        )
