from config.configuration_variables import LOCAL_LLM_HOST
from litellm_service.llm_requester import Requester
from ollama import Client


class OllamaRequester(Requester):
    def __init__(self, model):
        self._model_name = model

        self._client = Client(LOCAL_LLM_HOST)

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

        response = self._client.chat(model=self._model_name, messages=messages, format="json", *args, **kwargs)
        return self._model_name, {"choices": [response]}
