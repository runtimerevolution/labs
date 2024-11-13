import logging

from api.schemas import (
    ChangeIssueStatusRequest,
    CommitChangesRequest,
    CreateBranchRequest,
    CreatePullRequestRequest,
    GithubModel,
    IssueRequest,
    ListIssuesRequest,
)
from decorators import async_time_and_log_function
from django.http import HttpRequest
from github.github import GithubRequests
from ninja import Router
from ninja.errors import HttpError

logger = logging.getLogger(__name__)

router = Router(tags=["github"])


@router.post("/list-issues")
@async_time_and_log_function
async def list_issues(request: HttpRequest, github: GithubModel, params: ListIssuesRequest):
    try:
        github_requests = GithubRequests(
            github_token=github.github_token,
            repo_owner=github.repo_owner,
            repo_name=github.repo_name,
            username=github.username,
        )
        return github_requests.list_issues(assignee=params.assignee, state=params.state, per_page=params.per_page)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/get-issue")
@async_time_and_log_function
async def get_issue(request: HttpRequest, github: GithubModel, params: IssueRequest):
    try:
        github_requests = GithubRequests(
            github_token=github.github_token,
            repo_owner=github.repo_owner,
            repo_name=github.repo_name,
            username=github.username,
        )
        return github_requests.get_issue(issue_number=params.issue_number)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/create-branch")
@async_time_and_log_function
async def create_branch(request: HttpRequest, github: GithubModel, params: CreateBranchRequest):
    try:
        github_requests = GithubRequests(
            github_token=github.github_token,
            repo_owner=github.repo_owner,
            repo_name=github.repo_name,
            username=github.username,
        )
        return github_requests.create_branch(branch_name=params.branch_name, original_branch=params.original_branch)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/change-issue-status")
@async_time_and_log_function
async def change_issue_status(request: HttpRequest, github: GithubModel, params: ChangeIssueStatusRequest):
    try:
        github_requests = GithubRequests(
            github_token=github.github_token,
            repo_owner=github.repo_owner,
            repo_name=github.repo_name,
            username=github.username,
        )
        return github_requests.change_issue_status(issue_number=params.issue_number, state=params.state)
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/commit-changes")
@async_time_and_log_function
async def commit_changes(request: HttpRequest, github: GithubModel, params: CommitChangesRequest):
    try:
        github_requests = GithubRequests(
            github_token=github.github_token,
            repo_owner=github.repo_owner,
            repo_name=github.repo_name,
            username=github.username,
        )
        return github_requests.commit_changes(
            message=params.message, branch_name=params.branch_name, files=params.files
        )
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/create-pull-request")
@async_time_and_log_function
async def create_pull_request(request: HttpRequest, github: GithubModel, params: CreatePullRequestRequest):
    try:
        github_requests = GithubRequests(
            github_token=github.github_token,
            repo_owner=github.repo_owner,
            repo_name=github.repo_name,
            username=github.username,
        )
        return github_requests.create_pull_request(
            head=params.head, base=params.base, title=params.title, body=params.body
        )
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/clone")
@async_time_and_log_function
async def clone_repo(request: HttpRequest, github: GithubModel):
    try:
        github_requests = GithubRequests(
            github_token=github.github_token,
            repo_owner=github.repo_owner,
            repo_name=github.repo_name,
            username=github.username,
        )
        return github_requests.clone()
    except Exception as e:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(e))
