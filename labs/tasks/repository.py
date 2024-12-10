import json
from typing import List, cast

from decorators import time_and_log_function
from django.conf import settings
from github.github import GithubRequests
from parsers.response import create_file, modify_file, parse_llm_output
from tasks.redis_client import RedisStrictClient, RedisVariable

from config.celery import app

redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


def github_repository_data(prefix, token="", repository_owner="", repository_name="", username="") -> dict:
    return dict(
        token=redis_client.get(RedisVariable.TOKEN, prefix, default=token),
        repository_owner=redis_client.get(RedisVariable.REPOSITORY_OWNER, prefix, default=repository_owner),
        repository_name=redis_client.get(RedisVariable.REPOSITORY_NAME, prefix, default=repository_name),
        username=redis_client.get(RedisVariable.USERNAME, prefix, default=username),
    )


@time_and_log_function
def apply_code_changes(llm_response):
    response = parse_llm_output(llm_response)

    files: List[str | None] = []
    for step in response.steps:
        file_path = None
        if step.type == "create":
            file_path = files.append(create_file(path=step.path, content=step.content))
        elif step.type == "modify":
            file_path = files.append(
                modify_file(path=step.path, content=step.content, line_number=cast(int, step.line))
            )
        files.append(file_path)

    return files


@app.task
def get_issue_task(prefix="", token="", repository_owner="", repository_name="", issue_number="", username=""):
    repository = github_repository_data(prefix, token, repository_owner, repository_name, username)
    issue_number = redis_client.get(RedisVariable.ISSUE_NUMBER, prefix, default=issue_number)

    github_request = GithubRequests(**repository)
    issue = github_request.get_issue(issue_number)

    if prefix:
        redis_client.set(
            RedisVariable.ISSUE_TITLE,
            prefix=prefix,
            value=issue["title"].replace(" ", "-"),
            ex=300,
        )
        redis_client.set(
            RedisVariable.ISSUE_BODY,
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
    repository = github_repository_data(prefix, token, repository_owner, repository_name, username)
    issue_number = redis_client.get(RedisVariable.ISSUE_NUMBER, prefix, default=issue_number)
    original_branch = redis_client.get(RedisVariable.ORIGINAL_BRANCH_NAME, prefix, default=original_branch)
    issue_title = redis_client.get(RedisVariable.ISSUE_TITLE, prefix, default=issue_title)

    branch_name = f"{issue_number}-{issue_title}"

    github_request = GithubRequests(**repository)
    github_request.create_branch(branch_name=branch_name, original_branch=original_branch)

    if prefix:
        redis_client.set(RedisVariable.BRANCH_NAME, prefix=prefix, value=branch_name, ex=300)
        return prefix
    return branch_name


@app.task
def clone_repository_task(prefix="", repository_owner="", repository_name=""):
    repository = github_repository_data(prefix, repository_owner=repository_owner, repository_name=repository_name)

    github_request = GithubRequests(**repository)
    repository_path = github_request.clone()

    if prefix:
        redis_client.set(RedisVariable.REPOSITORY_PATH, prefix=prefix, value=repository_path, ex=300)
        return prefix
    return True


@app.task
def apply_code_changes_task(prefix="", llm_response=""):
    llm_response = redis_client.get(RedisVariable.LLM_RESPONSE, prefix, default=llm_response)
    modified_files = apply_code_changes(llm_response)

    if prefix:
        redis_client.set(RedisVariable.FILES_MODIFIED, prefix=prefix, value=json.dumps(modified_files))
        return prefix
    return modified_files


@app.task
def commit_changes_task(
    prefix="",
    token="",
    repository_owner="",
    repository_name="",
    username="",
    branch_name="",
    files_modified=None,
):
    if not files_modified:
        files_modified = []

    repository = github_repository_data(prefix, token, repository_owner, repository_name, username)
    github_request = GithubRequests(**repository)
    github_request.commit_changes(
        message="Fix",
        branch_name=redis_client.get(RedisVariable.BRANCH_NAME, prefix, default=branch_name),
        files=json.loads(redis_client.get(RedisVariable.FILES_MODIFIED, prefix, default=files_modified)),
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
    repository = github_repository_data(prefix, token, repository_owner, repository_name, username)
    github_request = GithubRequests(**repository)
    github_request.create_pull_request(
        head=redis_client.get(RedisVariable.BRANCH_NAME, prefix, default=branch_name),
        base=redis_client.get(RedisVariable.ORIGINAL_BRANCH_NAME, prefix, default=original_branch),
    )

    if prefix:
        return prefix
    return True
