import json
import logging
from types import SimpleNamespace

import config.configuration_variables as settings
from config.celery import app
from github.github import GithubRequests
from llm import apply_code_changes
from tasks.redis_client import RedisStrictClient, RedisVariables

logger = logging.getLogger(__name__)

redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


def get_redis_github_data(
    prefix, token="", repository_owner="", repository_name="", username="", as_namespace=False
) -> dict | SimpleNamespace:
    variables = dict(
        token=redis_client.get(RedisVariables.TOKEN, prefix, default=token),
        repository_owner=redis_client.get(RedisVariables.REPOSITORY_OWNER, prefix, default=repository_owner),
        repository_name=redis_client.get(RedisVariables.REPOSITORY_NAME, prefix, default=repository_name),
        username=redis_client.get(RedisVariables.USERNAME, prefix, default=username),
    )

    if as_namespace:
        return SimpleNamespace(**variables)

    return variables


@app.task
def get_issue_task(prefix="", token="", repository_owner="", repository_name="", issue_number="", username=""):
    github_request_data = get_redis_github_data(prefix, token, repository_owner, repository_name, username)
    issue_number = redis_client.get(RedisVariables.ISSUE_NUMBER, prefix, default=issue_number)

    github_request = GithubRequests(**github_request_data)
    issue = github_request.get_issue(issue_number)

    if prefix:
        redis_client.set(
            RedisVariables.ISSUE_TITLE,
            prefix=prefix,
            value=issue["title"].replace(" ", "-"),
            ex=300,
        )
        redis_client.set(
            RedisVariables.ISSUE_BODY,
            prefix=prefix,
            value=issue["body"],
            ex=300,
        )
        return prefix
    return issue


@app.task
def create_branch_task(
    prefix="",
    token="",
    repository_owner="",
    repository_name="",
    issue_number="",
    username="",
    original_branch="",
    issue_title="",
):
    github_request_data = get_redis_github_data(prefix, token, repository_owner, repository_name, username)
    issue_number = redis_client.get(RedisVariables.ISSUE_NUMBER, prefix, default=issue_number)
    original_branch = redis_client.get(RedisVariables.ORIGINAL_BRANCH_NAME, prefix, default=original_branch)
    issue_title = redis_client.get(RedisVariables.ISSUE_TITLE, prefix, default=issue_title)

    branch_name = f"{issue_number}-{issue_title}"

    github_request = GithubRequests(**github_request_data)
    github_request.create_branch(branch_name=branch_name, original_branch=original_branch)

    if prefix:
        redis_client.set(RedisVariables.BRANCH_NAME, prefix=prefix, value=branch_name, ex=300)
        return prefix
    return branch_name


@app.task
def clone_repository_task(prefix="", repository_owner="", repository_name=""):
    github_request_data = get_redis_github_data(
        prefix, repository_owner=repository_owner, repository_name=repository_name
    )

    github_request = GithubRequests(**github_request_data)
    repository_path = github_request.clone()

    if prefix:
        redis_client.set(RedisVariables.REPOSITORY_NAME, prefix=prefix, value=repository_path, ex=300)
        return prefix
    return True


@app.task
def apply_code_changes_task(prefix="", llm_response=""):
    llm_response = redis_client.get(RedisVariables.LLM_RESPONSE, prefix, default=llm_response)
    files_modified = apply_code_changes(llm_response)

    if prefix:
        redis_client.set(RedisVariables.FILES_MODIFIED, prefix=prefix, value=json.dumps(files_modified))
        return prefix
    return files_modified


@app.task
def commit_changes_task(
    prefix="",
    token="",
    repository_owner="",
    repository_name="",
    username="",
    branch_name="",
    files_modified=[],
):
    github_request_data = get_redis_github_data(prefix, token, repository_owner, repository_name, username)
    github_request = GithubRequests(**github_request_data)
    github_request.commit_changes(
        message="Fix",
        branch_name=redis_client.get(RedisVariables.BRANCH_NAME, prefix, default=branch_name),
        files=json.loads(redis_client.get(RedisVariables.FILES_MODIFIED, prefix, default=files_modified)),
    )

    if prefix:
        return prefix
    return True


@app.task
def create_pull_request_task(
    prefix="",
    token="",
    repository_owner="",
    repository_name="",
    username="",
    branch_name="",
    original_branch="",
):
    github_request_data = get_redis_github_data(prefix, token, repository_owner, repository_name, username)
    github_request = GithubRequests(**github_request_data)
    github_request.create_pull_request(
        head=redis_client.get(RedisVariables.BRANCH_NAME, prefix, default=branch_name),
        base=redis_client.get(RedisVariables.ORIGINAL_BRANCH_NAME, prefix, default=original_branch),
    )

    if prefix:
        return prefix
    return True
