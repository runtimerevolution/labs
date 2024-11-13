import json
import logging

import config.configuration_variables as settings
import redis
from config.celery import app
from repo import call_agent_to_apply_code_changes, clone_repository
from run import commit_changes, create_branch, create_pull_request, get_issue

logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


@app.task
def get_issue_task(prefix="", token="", repo_owner="", repo_name="", issue_number="", username=""):
    token = redis_client.get(f"{prefix}_token") if prefix else token
    repo_owner = redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner
    repo_name = redis_client.get(f"{prefix}_repo_name") if prefix else repo_name
    username = redis_client.get(f"{prefix}_username") if prefix else username
    issue_number = redis_client.get(f"{prefix}_issue_number") if prefix else issue_number

    issue = get_issue(token, repo_owner, repo_name, username, issue_number)

    if prefix:
        issue_title = issue["title"].replace(" ", "-")
        issue_body = issue["body"]
        redis_client.set(f"{prefix}_issue_title", issue_title, ex=300)
        redis_client.set(f"{prefix}_issue_body", issue_body, ex=300)
        return prefix
    return issue


@app.task
def create_branch_task(
    prefix="",
    token="",
    repo_owner="",
    repo_name="",
    issue_number="",
    username="",
    original_branch="",
    issue_title="",
):
    token = redis_client.get(f"{prefix}_token") if prefix else token
    repo_owner = redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner
    repo_name = redis_client.get(f"{prefix}_repo_name") if prefix else repo_name
    username = redis_client.get(f"{prefix}_username") if prefix else username
    issue_number = redis_client.get(f"{prefix}_issue_number") if prefix else issue_number
    original_branch = redis_client.get(f"{prefix}_original_branch") if prefix else original_branch
    issue_title = redis_client.get("issue_title") if prefix else issue_title

    branch_name = create_branch(
        token,
        repo_owner,
        repo_name,
        username,
        issue_number,
        issue_title,
        original_branch,
    )

    if prefix:
        redis_client.set(f"{prefix}_branch_name", branch_name, ex=300)
        return prefix
    return branch_name


@app.task
def clone_repo_task(prefix="", repo_owner="", repo_name=""):
    repo_owner = redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner
    repo_name = redis_client.get(f"{prefix}_repo_name") if prefix else repo_name
    repo_destination = f"{settings.CLONE_DESTINATION_DIR}{repo_owner}/{repo_name}"
    clone_repository(f"https://github.com/{repo_owner}/{repo_name}", repo_destination)

    if prefix:
        redis_client.set(f"{prefix}_repo_destination", repo_destination, ex=300)
        return prefix
    return True


@app.task
def apply_code_changes_task(prefix="", llm_response=""):
    llm_response = redis_client.get(f"{prefix}_llm_response") if prefix else llm_response
    files_modified = call_agent_to_apply_code_changes(llm_response)

    if prefix:
        redis_client.set(f"{prefix}_files_modified", json.dumps(files_modified))
        return prefix
    return files_modified


@app.task
def commit_changes_task(
    prefix="",
    token="",
    repo_owner="",
    repo_name="",
    username="",
    branch_name="",
    files_modified=[],
):
    commit_changes(
        token=redis_client.get(f"{prefix}_token") if prefix else token,
        repo_owner=redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner,
        repo_name=redis_client.get(f"{prefix}_repo_name") if prefix else repo_name,
        username=redis_client.get(f"{prefix}_username") if prefix else username,
        branch_name=(redis_client.get(f"{prefix}_branch_name") if prefix else branch_name),
        file_list=(json.loads(redis_client.get(f"{prefix}_files_modified")) if prefix else files_modified),
    )

    if prefix:
        return prefix
    return True


@app.task
def create_pull_request_task(
    prefix="",
    token="",
    repo_owner="",
    repo_name="",
    username="",
    branch_name="",
    original_branch="",
):
    create_pull_request(
        token=redis_client.get(f"{prefix}_token") if prefix else token,
        repo_owner=redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner,
        repo_name=redis_client.get(f"{prefix}_repo_name") if prefix else repo_name,
        username=redis_client.get(f"{prefix}_username") if prefix else username,
        original_branch=(redis_client.get(f"{prefix}_original_branch") if prefix else original_branch),
        branch_name=(redis_client.get(f"{prefix}_branch_name") if prefix else branch_name),
    )

    if prefix:
        return prefix
    return True
