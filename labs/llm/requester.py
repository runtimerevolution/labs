from typing import Any, Dict, List, Tuple


class Requester:
    def __init__(self, requester, *args, **kwargs):
        self.requester = requester(*args, **kwargs)

    def completion_without_proxy(
        self, messages: List[Dict[str, str]], *args, **kwargs
    ) -> Tuple[str, Dict[str, Any], int]:
        return self.requester.completion_without_proxy(messages, *args, **kwargs)
