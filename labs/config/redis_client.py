from enum import Enum
from typing import Union

from django.conf import settings
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
    PRE_COMMIT_ERROR = "pre_commit_error"
    PROMPT = "prompt"
    REPOSITORY_NAME = "repository_name"
    REPOSITORY_OWNER = "repository_owner"
    REPOSITORY_PATH = "repository_path"
    TOKEN = "token"
    USERNAME = "username"


class RedisStrictClient(StrictRedis):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RedisStrictClient, cls).__new__(cls)
        return cls._instance

    def get(
        self, variable: Union[str, RedisVariable], prefix: str = None, default: str | list | dict = None
    ) -> ResponseT:
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


redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
