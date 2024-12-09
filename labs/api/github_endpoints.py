import logging

from api.schemas.github import (
    BranchSchema,
    CommitSchema,
    GithubSchema,
    IssueSchema,
    IssueStatusSchema,
    ListIssuesSchema,
    PullRequestSchema,
)
from decorators import async_time_and_log_function
from django.http import HttpRequest
from github.github import GithubRequests
from ninja import Router
from ninja.errors import HttpError

logger = logging.getLogger(__name__)

router = Router(tags=["github"])


@router.post("/list_issues")
@async_time_and_log_function
async def list_issues_endpoint(request: HttpRequest, params: ListIssuesSchema):
    try:
        github_requests = GithubRequests(
            token=params.token,
            repository_owner=params.repository_owner,
            repository_name=params.repository_name,
            username=params.username,
        )
        return github_requests.list_issues(assignee=params.assignee, state=params.state, per_page=params.per_page)
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/get_issue")
@async_time_and_log_function
async def get_issue_endpoint(request: HttpRequest, params: IssueSchema):
    try:
        github_requests = GithubRequests(
            token=params.token,
            repository_owner=params.repository_owner,
            repository_name=params.repository_name,
            username=params.username,
        )
        return github_requests.get_issue(issue_number=params.issue_number)
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/create_branch")
@async_time_and_log_function
async def create_branch_endpoint(request: HttpRequest, params: BranchSchema):
    try:
        github_requests = GithubRequests(
            token=params.token,
            repository_owner=params.repository_owner,
            repository_name=params.repository_name,
            username=params.username,
        )
        return github_requests.create_branch(branch_name=params.branch_name, original_branch=params.original_branch)
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/change_issue_status")
@async_time_and_log_function
async def change_issue_status_endpoint(request: HttpRequest, params: IssueStatusSchema):
    try:
        github_requests = GithubRequests(
            token=params.token,
            repository_owner=params.repository_owner,
            repository_name=params.repository_name,
            username=params.username,
        )
        return github_requests.change_issue_status(issue_number=params.issue_number, status=params.status)
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/commit_changes")
@async_time_and_log_function
async def commit_changes_endpoint(request: HttpRequest, params: CommitSchema):
    try:
        github_requests = GithubRequests(
            token=params.token,
            repository_owner=params.repository_owner,
            repository_name=params.repository_name,
            username=params.username,
        )
        return github_requests.commit_changes(
            message=params.message, branch_name=params.branch_name, files=params.files
        )
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/create_pull_request")
@async_time_and_log_function
async def create_pull_request_endpoint(request: HttpRequest, params: PullRequestSchema):
    try:
        github_requests = GithubRequests(
            token=params.token,
            repository_owner=params.repository_owner,
            repository_name=params.repository_name,
            username=params.username,
        )
        return github_requests.create_pull_request(
            head=params.head_branch_name, base=params.base_branch_name, title=params.title, body=params.body
        )
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HttpError(status_code=500, message="Internal server error: " + str(e))


@router.post("/clone")
@async_time_and_log_function
async def clone_repository_endpoint(request: HttpRequest, params: GithubSchema):
    try:
        github_requests = GithubRequests(
            token=params.token,
            repository_owner=params.repository_owner,
            repository_name=params.repository_name,
            username=params.username,
        )
        return github_requests.clone()
    except Exception as e:
        logger.exception("Internal server error", exc_info=e)
        raise HttpError(status_code=500, message="Internal server error: " + str(e))
