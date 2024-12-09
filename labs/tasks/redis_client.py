from enum import Enum
from typing import Any, Union

from redis import StrictRedis
from redis.typing import EncodableT, ResponseT


class RedisVariable(Enum):
    BRANCH_NAME = "branch_name"
    CONTEXT = "context"
    EMBEDDINGS = "embeddings"
    FILES_MODIFIED = "files_modified"
    ISSUE_BODY = "issue_body"
    ISSUE_NUMBER = "issue_number"
    ISSUE_TITLE = "issue_title"
    LLM_RESPONSE = "llm_response"
    ORIGINAL_BRANCH_NAME = "original_branch_name"
    PROMPT = "prompt"
    REPOSITORY_NAME = "repository_name"
    REPOSITORY_OWNER = "repository_owner"
    REPOSITORY_PATH = "repository_path"
    TOKEN = "token"
    USERNAME = "username"


class RedisStrictClient(StrictRedis):
    def get(self, variable: Union[str, RedisVariable], prefix: str = None, default: str = None) -> ResponseT:
        name = variable
        if isinstance(variable, RedisVariable):
            name = variable.value

        if prefix:
            name = f"{prefix}_{name}"

        if self.exists(name):
            return super().get(name)
        return default

    def set(
        self,
        variable: Union[str, RedisVariable],
        value: EncodableT,
        prefix: str = None,
        *args,
        **kwargs,
    ) -> ResponseT:
        name = variable
        if isinstance(variable, RedisVariable):
            name = variable.value

        if prefix:
            name = f"{prefix}_{name}"

        return super().set(name, value, *args, **kwargs)
