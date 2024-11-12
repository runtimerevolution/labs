from ollama import Client

import config.configuration_variables as settings


class RequestLocalLLM:
    def __init__(self):
        self.client = Client(host=settings.LOCAL_LLM_HOST)

    def format_response(self, response):
        return {"choices": [response]}

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
        model = "llama3.2"
        response = self.client.chat(model=model, messages=messages, format="json")

        llm_response = self.format_response(response)

        return model, llm_response
