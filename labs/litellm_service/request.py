from litellm import completion
from pydantic import BaseModel
from labs.config import settings


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
    def __init__(self):
        self.api_key = settings.LITELLM_API_KEY

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
            return model, completion(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
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
