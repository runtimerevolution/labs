from typing import List, Optional
from pydantic import BaseModel


class GithubModel(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    user_name: Optional[str] = None


class CodeMonkeyRequest(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    issue_number: int
    user_name: Optional[str] = None
    litellm_api_key: str


class ListIssuesRequest(BaseModel):
    assignee: Optional[str] = None
    state: str = "open"
    per_page: int = 100


class ChangeIssueStatusRequest(BaseModel):
    issue_number: int
    state: str


class CreateBranchRequest(BaseModel):
    branch_name: str
    original_branch: str = "main"


class CommitChangesRequest(BaseModel):
    message: str
    branch_name: str
    files: List[str]


class CreatePullRequest(BaseModel):
    head: str
    base: str = "main"
    title: str = "New Pull Request"
    body: str = ""


class IssueRequest(BaseModel):
    issue_number: int


class CallLLMRequest(BaseModel):
    issue_summary: str
    token: str
