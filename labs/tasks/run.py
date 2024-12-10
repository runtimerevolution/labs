import os.path

import config.configuration_variables as settings
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
from tasks.redis_client import RedisStrictClient, RedisVariable

redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


@app.task(bind=True)
def init_task(self, **kwargs):
    path = RedisVariable.REPOSITORY_PATH.value
    if path in kwargs and not os.path.exists(kwargs[path]):
        raise FileNotFoundError(f"Directory {kwargs[path]} does not exist")

    prefix = self.request.id
    for k, v in kwargs.items():
        redis_client.set(k, v, prefix=prefix, ex=3600)
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
        RedisVariable.TOKEN.value: token,
        RedisVariable.REPOSITORY_OWNER.value: repository_owner,
        RedisVariable.REPOSITORY_NAME.value: repository_name,
        RedisVariable.USERNAME.value: username,
        RedisVariable.ISSUE_NUMBER.value: issue_number,
        RedisVariable.ORIGINAL_BRANCH_NAME.value: original_branch,
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
def run_on_local_repository_task(repository_path, issue_body):
    data = {
        RedisVariable.ISSUE_BODY.value: issue_body,
        RedisVariable.REPOSITORY_PATH.value: repository_path,
    }
    chain(
        init_task.s(**data),
        vectorize_repository_task.s(),
        find_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
    ).apply_async()
