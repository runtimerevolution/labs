import logging

from api.schemas.codemonkey import (
    ApplyCodeChangesSchema,
    FindEmbeddingsSchema,
    GithubRepositorySchema,
    LLMReponseSchema,
    LocalRepositoryShema,
    PreparePromptContextSchema,
    VectorizeRepositorySchema,
)
from api.schemas.github import BranchIssueSchema, CommitSchema, IssueSchema, PullRequestSchema
from asgiref.sync import sync_to_async
from decorators import async_time_and_log_function
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from tasks import (
    apply_code_changes_task,
    commit_changes_task,
    create_branch_task,
    create_pull_request_task,
    find_embeddings_task,
    get_issue_task,
    get_llm_response_task,
    prepare_prompt_and_context_task,
    run_on_local_repository_task,
    run_on_repository_task,
    vectorize_repository_task,
)

logger = logging.getLogger(__name__)

router = Router(tags=["codemonkey"])


@router.post("/run_on_repository")
@async_time_and_log_function
async def run_on_repository_endpoint(request: HttpRequest, run_on_repository: GithubRepositorySchema):
    try:
        run_on_repository_task(
            token=run_on_repository.token,
            repository_owner=run_on_repository.repository_owner,
            repository_name=run_on_repository.repository_name,
            issue_number=run_on_repository.issue_number,
            username=run_on_repository.username,
            original_branch=run_on_repository.original_branch,
        )
    except Exception as ex:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(ex))


@router.post("/run_on_local_repository", response={200: None})
@async_time_and_log_function
async def run_on_local_repository_endpoint(request: HttpRequest, run_on_local_repository: LocalRepositoryShema):
    try:
        run_on_local_repository_task(
            repository_path=run_on_local_repository.repository_path, issue_body=run_on_local_repository.prompt
        )
    except Exception as ex:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(ex))


@router.post("/vectorize_repository")
@async_time_and_log_function
async def vectorize_repository_endpoint(request: HttpRequest, vectorize_repository: VectorizeRepositorySchema):
    return await sync_to_async(vectorize_repository_task, thread_sensitive=True)(
        repository_path=vectorize_repository.repository_path
    )


@router.post("/find_embeddings")
@async_time_and_log_function
async def find_embeddings_endpoint(request: HttpRequest, find_embeddings: FindEmbeddingsSchema):
    return await sync_to_async(find_embeddings_task, thread_sensitive=True)(
        issue_body=find_embeddings.prompt, repository_path=find_embeddings.repository_path
    )


@router.post("/prepare_prompt_and_context")
@async_time_and_log_function
async def prepare_prompt_and_context_endpoint(request: HttpRequest, prepare_prompt_context: PreparePromptContextSchema):
    return await sync_to_async(prepare_prompt_and_context_task, thread_sensitive=True)(
        issue_body=prepare_prompt_context.prompt, embeddings=prepare_prompt_context.embeddings
    )


@router.post("/get_llm_response")
@async_time_and_log_function
async def get_llm_response_endpoint(request: HttpRequest, llm_reponse: LLMReponseSchema):
    return await sync_to_async(get_llm_response_task, thread_sensitive=True)(context=llm_reponse.context)


@router.post("/apply_code_changes")
@async_time_and_log_function
async def apply_code_changes_endpoint(request: HttpRequest, apply_code_changes: ApplyCodeChangesSchema):
    return await sync_to_async(apply_code_changes_task, thread_sensitive=True)(llm_response=apply_code_changes.changes)


@router.post("/get_issue")
@async_time_and_log_function
async def get_issue_endpoint(request: HttpRequest, issue: IssueSchema):
    return get_issue_task(
        token=issue.token,
        repository_owner=issue.repository_owner,
        repository_name=issue.repository_name,
        username=issue.username,
        issue_number=issue.issue_number,
    )


@router.post("/create_branch")
@async_time_and_log_function
async def create_branch_endpoint(request: HttpRequest, branch: BranchIssueSchema):
    return create_branch_task(
        token=branch.token,
        repository_owner=branch.repository_owner,
        repository_name=branch.repository_name,
        username=branch.username,
        issue_number=branch.issue_number,
        original_branch=branch.original_branch,
        issue_title=branch.issue_title,
    )


@router.post("/commit_changes")
@async_time_and_log_function
async def commit_changes_endpoint(request: HttpRequest, commit: CommitSchema):
    return await sync_to_async(commit_changes_task, thread_sensitive=True)(
        token=commit.token,
        repository_owner=commit.repository_owner,
        repository_name=commit.repository_name,
        username=commit.username,
        branch_name=commit.branch_name,
        files_modified=commit.files,
    )


@router.post("/create_pull_request")
@async_time_and_log_function
async def create_pull_request_endpoint(request: HttpRequest, pull_request: PullRequestSchema):
    return await sync_to_async(create_pull_request_task, thread_sensitive=True)(
        token=pull_request.token,
        repository_owner=pull_request.repository_owner,
        repository_name=pull_request.repository_name,
        username=pull_request.username,
        branch_name=pull_request.changes_branch_name,
        original_branch=pull_request.base_branch_name,
    )
