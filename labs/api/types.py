from typing import Optional
from pydantic import BaseModel


class GithubModel(BaseModel):
    token: str
    repo_owner: str
    repo_name: str
    username: str


class RunOnRepoRequest(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    username: str
    issue_number: int
    original_branch: Optional[str] = "main"
    model: Optional[str] = None


class RunOnLocalRepoRequest(BaseModel):
    repo_path: str
    issue_text: str


class GetIssueRequest(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    username: str
    issue_number: int


class CreateBranchRequest(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    username: str
    issue_number: int
    original_branch: str
    issue_title: str


class VectorizeRepoToDatabaseRequest(BaseModel):
    repo_destination: str


class FindSimilarEmbeddingsRequest(BaseModel):
    issue_body: str


class PreparePromptAndContextRequest(BaseModel):
    issue_body: str
    embeddings: list


class GetLLMResponseRequest(BaseModel):
    context: dict


class ApplyCodeChangesRequest(BaseModel):
    llm_response: str


class ListIssuesRequest(BaseModel):
    assignee: Optional[str] = None
    state: str = "open"
    per_page: int = 100


class ChangeIssueStatusRequest(BaseModel):
    issue_number: int
    state: str


class CommitChangesRequest(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    username: str
    branch_name: str
    files: list


class CreatePullRequestRequest(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    username: str
    original_branch: str
    branch_name: str


class IssueRequest(BaseModel):
    issue_number: int


class CallLLMRequest(BaseModel):
    issue_summary: str
    token: str
