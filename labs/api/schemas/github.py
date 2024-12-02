from typing import List, Optional

from pydantic import BaseModel


class GithubSchema(BaseModel):
    token: str
    repository_owner: str
    repository_name: str
    username: str


class IssueSchema(GithubSchema):
    issue_number: int


class BranchSchema(GithubSchema):
    original_branch: str = "main"
    branch_name: str


class BranchIssueSchema(IssueSchema):
    original_branch: str = "main"
    issue_title: str


class ListIssuesSchema(GithubSchema):
    assignee: Optional[str] = None
    state: str = "open"
    per_page: int = 100


class IssueStatusSchema(GithubSchema):
    issue_number: int
    status: str


class CommitSchema(GithubSchema):
    message: Optional[str] = None
    branch_name: str
    files: List[str]


class PullRequestSchema(GithubSchema):
    changes_branch_name: str
    base_branch_name: str
    title: Optional[str] = None
    body: Optional[str] = None
