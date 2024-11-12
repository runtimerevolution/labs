import logging

from ninja import Router
from ninja.errors import HttpError

from labs.api.schemas import (
    ChangeIssueStatusRequest,
    CommitChangesRequest,
    CreateBranchRequest,
    CreatePullRequestRequest,
    GithubModel,
    IssueRequest,
    ListIssuesRequest,
)
from labs.decorators import async_time_and_log_function
from labs.github.github import GithubRequests

logger = logging.getLogger(__name__)

router = Router(tags=["github"])


@router.post("/github/list-issues")
@async_time_and_log_function
async def list_issues(request: GithubModel, params: ListIssuesRequest):
    try:
        github_requests = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )
        return github_requests.list_issues(assignee=params.assignee, state=params.state, per_page=params.per_page)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/github/get-issue")
@async_time_and_log_function
async def get_issue(request: GithubModel, params: IssueRequest):
    try:
        github_requests = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )
        return github_requests.get_issue(issue_number=params.issue_number)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/github/create-branch")
@async_time_and_log_function
async def create_branch(request: GithubModel, params: CreateBranchRequest):
    try:
        github_requests = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )
        return github_requests.create_branch(branch_name=params.branch_name, original_branch=params.original_branch)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/github/change-issue-status")
@async_time_and_log_function
async def change_issue_status(request: GithubModel, params: ChangeIssueStatusRequest):
    try:
        github_requests = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )
        return github_requests.change_issue_status(issue_number=params.issue_number, state=params.state)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/github/commit-changes")
@async_time_and_log_function
async def commit_changes(request: GithubModel, params: CommitChangesRequest):
    try:
        github_requests = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )
        return github_requests.commit_changes(
            message=params.message, branch_name=params.branch_name, files=params.files
        )
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/github/create-pull-request")
@async_time_and_log_function
async def create_pull_request(request: GithubModel, params: CreatePullRequestRequest):
    try:
        github_requests = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )
        return github_requests.create_pull_request(
            head=params.head, base=params.base, title=params.title, body=params.body
        )
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/github/clone")
@async_time_and_log_function
async def clone_repo(request: GithubModel):
    try:
        github_requests = GithubRequests(
            github_token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            username=request.username,
        )
        return github_requests.clone()
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))
