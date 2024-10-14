from litellm import completion, get_supported_openai_params
import requests
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Step(BaseModel):
    type: str
    path: str
    content: str


class PullRequest(BaseModel):
    steps: list[Step]


models = [
    "openai/gpt-4o",
    "cohere/command-light",
    "gemini/gemini-pro",
    "groq/llama3-8b-8192",
    "huggingface/tiiuae/falcon-7b-instruct",
]


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

    def completion_without_proxy(self, messages, model=None):
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
        if model:
            logger.debug("MODEL: %s", model)
            if self.__is_param_supported_by_model(model, "response_format"):
                return model, completion(
                    model=model,
                    messages=messages,
                    response_format={"type": "json_object"},
                )
            else:
                logger.debug("Parameter response_format is not supported.")
                return model, completion(
                    model=model,
                    messages=messages,
                )

        for model in models:
            try:
                response = completion(
                    model=model,
                    messages=messages,
                    response_format={"type": "json_object"},
                )
                return model, response
            except Exception:
                pass
        return model, None
    
    def __is_param_supported_by_model(self, model, param):
        supported_params = get_supported_openai_params(model=model)
        if param in supported_params:
            return True
        return False
