import os
import requests


class RequestLiteLLM:
    def __init__(self):
        self.api_key = os.environ.get("LITELLM_API_KEY", None)
        if not self.api_key:
            raise Exception("LITELLM_API_KEY missing.")

    def completion(self, messages, model="llm-model"):
        headers = {
            "Accept": "application/json",
            "API-Key": self.api_key,
        }

        data = {"messages": [{"role": "user", "content": message} for message in messages]}
        result = requests.post(
            f"http://0.0.0.0:4000/chat/completions?model={model}",
            headers=headers,
            json=data,
        )

        return result.json()["choices"][0]["message"]["content"]


# print(RequestLiteLLM().completion(messages=["Say hello."]))
