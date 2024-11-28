import logging
import os.path

import config.configuration_variables as settings
import redis
from celery import chain
from config.celery import app
from tasks import (
    apply_code_changes_task,
    clone_repository_task,
    commit_changes_task,
    create_branch_task,
    create_pull_request_task,
    find_embeddings_task,
    get_issue_task,
    get_llm_response_task,
    prepare_prompt_and_context_task,
    vectorize_repository_task,
)

logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


@app.task(bind=True)
def init_task(self, **kwargs):
    if "repository_path" in kwargs:
        if not os.path.exists(kwargs["repository_path"]):
            raise FileNotFoundError(f"Directory {kwargs['repository_path']} does not exist")
    prefix = self.request.id
    for k, v in kwargs.items():
        redis_client.set(f"{prefix}_{k}", v, ex=3600)
    return prefix


@app.task
def run_on_repository_task(
    token: str,
    repository_owner: str,
    repository_name: str,
    username: str,
    issue_number: int,
    original_branch: str = "main",
):
    data = {
        "token": token,
        "repository_owner": repository_owner,
        "repository_name": repository_name,
        "username": username,
        "issue_number": issue_number,
        "original_branch": original_branch,
    }
    chain(
        init_task.s(**data),
        get_issue_task.s(),
        create_branch_task.s(),
        clone_repository_task.s(),
        vectorize_repository_task.s(),
        find_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
        commit_changes_task.s(),
        create_pull_request_task.s(),
    ).apply_async()


@app.task
def run_on_local_repository_task(repository_path, issue_text):
    data = {
        "issue_text": issue_text,
        "issue_body": issue_text,
        "repository_path": repository_path,
    }
    chain(
        init_task.s(**data),
        vectorize_repository_task.s(),
        find_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
    ).apply_async()
