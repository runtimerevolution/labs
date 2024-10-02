from typing import List, Optional
from pydantic import BaseModel


class GithubModel(BaseModel):
    token: str
    repo_owner: str
    repo_name: str
    username: Optional[str] = None


class CodeMonkeyRequest(BaseModel):
    github_token: str
    repo_owner: str
    repo_name: str
    issue_number: int
    username: Optional[str] = None
    original_branch: Optional[str] = None


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
