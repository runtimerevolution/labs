from typing import Dict, List


class Requester:
    def __init__(self, requester, *args, **kwargs):
        self.requester = requester(*args, **kwargs)

    def completion_without_proxy(self, messages: List[Dict[str, str]], *args, **kwargs):
        return self.requester.completion_without_proxy(messages, *args, **kwargs)
