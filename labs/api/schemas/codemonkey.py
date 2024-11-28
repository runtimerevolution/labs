from typing import List, Optional

from api.schemas.github import GithubSchema
from pydantic import BaseModel


class GithubRepositorySchema(GithubSchema):
    issue_number: int
    original_branch: Optional[str] = None


class LocalRepositoryShema(BaseModel):
    repository_path: str
    prompt: str


class VectorizeRepositorySchema(BaseModel):
    repository_path: str


class FindEmbeddingsSchema(LocalRepositoryShema): ...


class PreparePromptContextSchema(BaseModel):
    prompt: str
    embeddings: List[List[str]]


class LLMReponseSchema(BaseModel):
    context: dict


class ApplyCodeChangesSchema(BaseModel):
    changes: str
