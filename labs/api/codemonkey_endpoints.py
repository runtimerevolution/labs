import logging

from api.schemas import (
    ApplyCodeChangesRequest,
    CommitChangesRequest,
    CreateBranchRequest,
    CreatePullRequestRequest,
    FindSimilarEmbeddingsRequest,
    GetIssueRequest,
    GetLLMResponseRequest,
    PreparePromptAndContextRequest,
    RunOnLocalRepoRequest,
    RunOnRepoRequest,
    VectorizeRepoToDatabaseRequest,
)
from decorators import async_time_and_log_function, time_and_log_function
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from tasks import (
    apply_code_changes_task,
    commit_changes_task,
    create_branch_task,
    create_pull_request_task,
    find_similar_embeddings_task,
    get_issue_task,
    get_llm_response_task,
    prepare_prompt_and_context_task,
    run_on_local_repo_task,
    run_on_repo_task,
    vectorize_repo_to_database_task,
)

logger = logging.getLogger(__name__)

router = Router(tags=["codemonkey"])


@router.post("/run_on_repo")
@async_time_and_log_function
async def run_on_repo_endpoint(request: HttpRequest, run_on_repo: RunOnRepoRequest):
    try:
        run_on_repo_task(
            token=run_on_repo.github_token,
            repo_owner=run_on_repo.repo_owner,
            repo_name=run_on_repo.repo_name,
            issue_number=run_on_repo.issue_number,
            username=run_on_repo.username,
            original_branch=run_on_repo.original_branch,
        )
    except Exception as ex:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(ex))


@router.post("/run_on_local_repo", response={200: None})
@async_time_and_log_function
async def run_on_local_repo_endpoint(request: HttpRequest, run_on_local_repo: RunOnLocalRepoRequest):
    try:
        run_on_local_repo_task(repo_path=run_on_local_repo.repo_path, issue_text=run_on_local_repo.issue_text)
    except Exception as ex:
        logger.exception("Internal server error")
        raise HttpError(status_code=500, message="Internal server error: " + str(ex))


@router.post("/get_issue")
@async_time_and_log_function
async def get_issue_endpoint(request: HttpRequest, get_issue: GetIssueRequest):
    return get_issue_task(
        token=get_issue.github_token,
        repo_owner=get_issue.repo_owner,
        repo_name=get_issue.repo_name,
        issue_number=get_issue.issue_number,
        username=get_issue.username,
    )


@router.post("/create_branch")
@async_time_and_log_function
async def create_branch_endpoint(request: HttpRequest, create_branch: CreateBranchRequest):
    return create_branch_task(
        token=create_branch.github_token,
        repo_owner=create_branch.repo_owner,
        repo_name=create_branch.repo_name,
        issue_number=create_branch.issue_number,
        username=create_branch.username,
        original_branch=create_branch.original_branch,
        issue_title=create_branch.issue_title,
    )


@router.post("/vectorize_repo_to_database")
@async_time_and_log_function
async def vectorize_repo_to_database_endpoint(
    request: HttpRequest, vectorize_repo_to_database: VectorizeRepoToDatabaseRequest
):
    return vectorize_repo_to_database_task(repo_destination=vectorize_repo_to_database.repo_destination)


@router.post("/find_similar_embeddings")
@async_time_and_log_function
async def find_similar_embeddings_endpoint(request: HttpRequest, find_similar_embeddings: FindSimilarEmbeddingsRequest):
    return find_similar_embeddings_task(issue_body=find_similar_embeddings.issue_body)


@router.post("/prepare_prompt_and_context")
@async_time_and_log_function
async def prepare_prompt_and_context_endpoint(
    request: HttpRequest, prepare_prompt_and_context: PreparePromptAndContextRequest
):
    return prepare_prompt_and_context_task(
        issue_body=prepare_prompt_and_context.issue_body, embeddings=prepare_prompt_and_context.embeddings
    )


@router.post("/get_llm_response")
@async_time_and_log_function
async def get_llm_response_endpoint(request: HttpRequest, get_llm_reponse: GetLLMResponseRequest):
    return get_llm_response_task(prepared_context=get_llm_reponse.context)


@router.post("/apply_code_changes")
@async_time_and_log_function
async def apply_code_changes_endpoint(request: HttpRequest, apply_code_changes: ApplyCodeChangesRequest):
    return apply_code_changes_task(llm_response=apply_code_changes.llm_response)


@router.post("/commit_changes")
@async_time_and_log_function
async def commit_changes_endpoint(request: HttpRequest, commit_changes: CommitChangesRequest):
    return commit_changes_task(
        token=commit_changes.github_token,
        repo_owner=commit_changes.repo_owner,
        repo_name=commit_changes.repo_name,
        username=commit_changes.username,
        branch_name=commit_changes.branch_name,
        files_modified=commit_changes.files,
    )


@router.post("/create_pull_request")
@async_time_and_log_function
async def create_pull_request_endpoint(request: HttpRequest, create_pull_request: CreatePullRequestRequest):
    return create_pull_request_task(
        token=create_pull_request.github_token,
        repo_owner=create_pull_request.repo_owner,
        repo_name=create_pull_request.repo_name,
        username=create_pull_request.username,
        branch_name=create_pull_request.branch_name,
        original_branch=create_pull_request.original_branch,
    )
