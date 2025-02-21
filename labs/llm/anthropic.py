import logging
import os
from typing import Any, Dict, List, Tuple, cast

from anthropic import Anthropic
from anthropic.types import Message, TextBlock

logger = logging.getLogger(__name__)


class AnthropicRequester:
    def __init__(self, model: str):
        self._model_name = model
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key)

    def completion_without_proxy(
        self,
        messages: List[Dict[str, str]],
        *args,
        **kwargs,
    ) -> Tuple[str, Dict[str, Any]]:
        system_prompt = "\n".join([message["content"] for message in messages if message["role"] == "system"])
        user_messages = [message for message in messages if message["role"] == "user"]

        try:
            response = self.client.messages.create(
                model=self._model_name, system=system_prompt, messages=user_messages, max_tokens=8192
            )

            response_steps = self.response_to_steps(response)

            return self._model_name, {"choices": [{"message": {"content": response_steps}}]}
        except Exception as e:
            raise RuntimeError(f"Anthropic API call failed: {e}") from e

    @staticmethod
    def response_to_steps(response: Message) -> str:
        response_text = str(cast(TextBlock, response.content[0]).text)

        json_start = response_text.index("{")
        json_end = response_text.rfind("}")

        steps = response_text[json_start : json_end + 1]

        return steps
