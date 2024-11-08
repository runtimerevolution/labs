import logging

import redis
from celery import chain

import labs.config.configuration_variables as settings
from labs.config.celery import app
from labs.tasks import (
    apply_code_changes_task,
    clone_repo_task,
    commit_changes_task,
    create_branch_task,
    create_pull_request_task,
    find_similar_embeddings_task,
    get_issue_task,
    get_llm_response_task,
    prepare_prompt_and_context_task,
    vectorize_repo_to_database_task,
)

logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


@app.task(bind=True)
def init_task(self, **kwargs):
    prefix = self.request.id
    for k, v in kwargs.items():
        redis_client.set(f"{prefix}_{k}", v, ex=3600)
    return prefix


@app.task
def run_on_repo_task(
    token: str,
    repo_owner: str,
    repo_name: str,
    username: str,
    issue_number: int,
    original_branch: str = "main",
):
    data = {
        "token": token,
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "username": username,
        "issue_number": issue_number,
        "original_branch": original_branch,
    }
    chain(
        init_task.s(**data),
        get_issue_task.s(),
        create_branch_task.s(),
        clone_repo_task.s(),
        vectorize_repo_to_database_task.s(),
        find_similar_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
        commit_changes_task.s(),
        create_pull_request_task.s(),
    ).apply_async()


@app.task
def run_on_local_repo_task(repo_path, issue_text):
    data = {
        "repo_path": repo_path,
        "issue_text": issue_text,
        "issue_body": issue_text,
        "repo_destination": repo_path,
    }
    chain(
        init_task.s(**data),
        vectorize_repo_to_database_task.s(),
        find_similar_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
    ).apply_async()
