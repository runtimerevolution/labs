from fastapi import APIRouter

from labs.api.types import (
    ChangeIssueStatusRequest,
    CommitChangesRequest,
    CreateBranchRequest,
    CreatePullRequest,
    GithubModel,
    IssueRequest,
    ListIssuesRequest,
)
from labs.github.github import GithubRequests

router = APIRouter()


@router.post("/github/list-issues")
async def list_issues(request: GithubModel, params: ListIssuesRequest):
    github_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        user_name=request.user_name,
    )
    return github_requests.list_issues(
        assignee=params.assignee, state=params.state, per_page=params.per_page
    )


@router.post("/github/get-issue")
async def get_issue(request: GithubModel, params: IssueRequest):
    github_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        user_name=request.user_name,
    )
    return github_requests.get_issue(issue_number=params.issue_number)


@router.post("/github/create-branch")
async def create_branch(request: GithubModel, params: CreateBranchRequest):
    github_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        user_name=request.user_name,
    )
    return github_requests.create_branch(
        branch_name=params.branch_name, original_branch=params.original_branch
    )


@router.post("/github/change-issue-status")
async def change_issue_status(request: GithubModel, params: ChangeIssueStatusRequest):
    github_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        user_name=request.user_name,
    )
    return github_requests.change_issue_status(
        issue_number=params.issue_number, state=params.state
    )


@router.post("/github/commit-changes")
async def commit_changes(request: GithubModel, params: CommitChangesRequest):
    github_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        user_name=request.user_name,
    )
    return github_requests.commit_changes(
        message=params.message, branch_name=params.branch_name, files=params.files
    )


@router.post("/github/create-pull-request")
async def create_pull_request(request: GithubModel, params: CreatePullRequest):
    github_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        user_name=request.user_name,
    )
    return github_requests.create_pull_request(
        head=params.head, base=params.base, title=params.title, body=params.body
    )


@router.post("/github/clone")
async def clone_repo(request: GithubModel):
    github_requests = GithubRequests(
        github_token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        user_name=request.user_name,
    )
    return github_requests.clone()
