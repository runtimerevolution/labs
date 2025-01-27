from typing import List, Optional

from api.schemas.github import GithubSchema
from django.conf import settings
from pydantic import BaseModel


class GithubRepositorySchema(GithubSchema):
    issue_number: int
    original_branch: Optional[str] = None


class LocalRepositoryShema(BaseModel):
    project_id: int
    prompt: str


class VectorizeRepositorySchema(BaseModel):
    project_id: int


class FindEmbeddingsSchema(LocalRepositoryShema):
    similarity_threshold: float = settings.EMBEDDINGS_SIMILARITY_THRESHOLD
    max_results: int = settings.EMBEDDINGS_MAX_RESULTS


class PreparePromptContextSchema(BaseModel):
    project_id: int
    prompt: str
    embeddings: List[List[str]]


class LLMReponseSchema(BaseModel):
    context: dict


class ApplyCodeChangesSchema(BaseModel):
    changes: str
