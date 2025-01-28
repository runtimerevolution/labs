from celery import chain
from config.celery import app
from config.redis_client import RedisVariable, redis_client
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
    run_pre_commit,
    save_workflow_result_task,
    vectorize_repository_task,
)


@app.task(bind=True)
def init_task(self, **kwargs):
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
        run_pre_commit.s(),
        commit_changes_task.s(),
        create_pull_request_task.s(),
        save_workflow_result_task.s(),
    ).apply_async(link_error=save_workflow_result_task.s())


@app.task
def run_on_local_repository_task(project_id, project_path, issue_body):
    data = {
        RedisVariable.PROJECT.value: project_id,
        RedisVariable.PROJECT_PATH.value: project_path,
        RedisVariable.ISSUE_BODY.value: issue_body,
    }
    chain(
        init_task.s(**data),
        vectorize_repository_task.s(),
        find_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
        run_pre_commit.s(),
        save_workflow_result_task.s(),
    ).apply_async(link_error=save_workflow_result_task.s())
