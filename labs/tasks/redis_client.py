from enum import Enum
from typing import Any, Union

from redis import StrictRedis
from redis.typing import AbsExpiryT, EncodableT, ExpiryT, ResponseT


class RedisVariables(Enum):
    TOKEN = "token"
    REPOSITORY_OWNER = "repository_owner"
    REPOSITORY_NAME = "repository_name"
    REPOSITORY_PATH = "repository_path"
    USERNAME = "username"
    ISSUE_NUMBER = "issue_number"
    ISSUE_TITLE = "issue_title"
    ISSUE_BODY = "issue_body"
    ORIGINAL_BRANCH_NAME = "original_branch_name"
    BRANCH_NAME = "branch_name"
    LLM_RESPONSE = "llm_response"
    FILES_MODIFIED = "files_modified"


class RedisStrictClient(StrictRedis):
    def get(
        self, variable: Union[str, RedisVariables], prefix: str = None, sufix: str = None, default: Any = None
    ) -> ResponseT:
        name = variable.value if isinstance(variable, RedisVariables) else variable
        if prefix:
            name = f"{prefix}_{name}"

        if sufix:
            name = f"{name}_{sufix}"

        if self.exists(name):
            return super().get(name)

        return default

    def set(
        self,
        variable: Union[str, RedisVariables],
        value: EncodableT,
        prefix: str = None,
        sufix: str = None,
        ex: Union[ExpiryT, None] = None,
        px: Union[ExpiryT, None] = None,
        nx: bool = False,
        xx: bool = False,
        keepttl: bool = False,
        get: bool = False,
        exat: Union[AbsExpiryT, None] = None,
        pxat: Union[AbsExpiryT, None] = None,
    ) -> ResponseT:
        name = variable.value if isinstance(variable, RedisVariables) else variable
        if prefix:
            name = f"{prefix}_{name}"

        if sufix:
            name = f"{name}_{sufix}"

        return super().set(name, value, ex, px, nx, xx, keepttl, get, exat, pxat)
