import os
import requests
from litellm import completion


class RequestLiteLLM:
    def __init__(self, litellm_api_key):
        self.api_key = litellm_api_key

    def completion(self, messages, model="llm-model"):
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
        headers = {
            "Accept": "application/json",
            "API-Key": self.api_key,
        }

        data = {"messages": messages}
        result = requests.post(
            f"http://0.0.0.0:4000/chat/completions?model={model}",
            headers=headers,
            json=data,
        )

        return result.json()

    def completion_without_proxy(self, messages, model="llm-model"):
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
        response = completion(
            model="openai/gpt-3.5-turbo",
            messages=messages,
        )
        return response
