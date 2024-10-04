from fastapi import APIRouter, HTTPException
from labs.api.types import (
    ApplyCodeChangesRequest,
    CommitChangesRequest,
    CreateBranchRequest,
    CreatePullRequestRequest,
    FindSimilarEmbeddingsRequest,
    GetIssueRequest,
    GetLLMResponseRequest,
    PreparePromptAndContextRequest,
    RunOnRepoRequest,
    RunOnLocalRepoRequest,
    VectorizeRepoToDatabaseRequest,
)
from labs.celery import (
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
from labs.decorators import async_time_and_log_function
import logging


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/codemonkey/run_on_repo")
@async_time_and_log_function
async def run_on_repo_endpoint(request: RunOnRepoRequest):
    try:
        run_on_repo_task(
            token=request.github_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            issue_number=request.issue_number,
            username=request.username,
            original_branch=request.original_branch,
        )
    except Exception as ex:
        logger.exception("Internal server error")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(ex))


@router.post("/codemonkey/run_on_local_repo")
@async_time_and_log_function
async def run_on_local_repo_endpoint(request: RunOnLocalRepoRequest):
    try:
        run_on_local_repo_task(repo_path=request.repo_path, issue_text=request.issue_text)
    except Exception as ex:
        logger.exception("Internal server error")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(ex))


@router.post("/codemonkey/get_issue")
@async_time_and_log_function
async def get_issue_endpoint(request: GetIssueRequest):
    return get_issue_task(
        token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        issue_number=request.issue_number,
        username=request.username,
    )


@router.post("/codemonkey/create_branch")
@async_time_and_log_function
async def create_branch_endpoint(request: CreateBranchRequest):
    return create_branch_task(
        token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        issue_number=request.issue_number,
        username=request.username,
        original_branch=request.original_branch,
        issue_title=request.issue_title,
    )


@router.post("/codemonkey/vectorize_repo_to_database")
@async_time_and_log_function
async def vectorize_repo_to_database_endpoint(request: VectorizeRepoToDatabaseRequest):
    return vectorize_repo_to_database_task(repo_destination=request.repo_destination)


@router.post("/codemonkey/find_similar_embeddings")
@async_time_and_log_function
async def find_similar_embeddings_endpoint(request: FindSimilarEmbeddingsRequest):
    return find_similar_embeddings_task(issue_body=request.issue_body)


@router.post("/codemonkey/prepare_prompt_and_context")
@async_time_and_log_function
async def prepare_prompt_and_context_endpoint(request: PreparePromptAndContextRequest):
    return prepare_prompt_and_context_task(issue_body=request.issue_body, embeddings=request.embeddings)


@router.post("/codemonkey/get_llm_response")
@async_time_and_log_function
async def get_llm_response_endpoint(request: GetLLMResponseRequest):
    return get_llm_response_task(prepared_context=request.context)


@router.post("/codemonkey/apply_code_changes")
@async_time_and_log_function
async def apply_code_changes_endpoint(request: ApplyCodeChangesRequest):
    return apply_code_changes_task(llm_response=request.llm_response)


@router.post("/codemonkey/commit_changes")
@async_time_and_log_function
async def commit_changes_endpoint(request: CommitChangesRequest):
    return commit_changes_task(
        token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        username=request.username,
        branch_name=request.branch_name,
        files_modified=request.files,
    )


@router.post("/codemonkey/create_pull_request")
@async_time_and_log_function
async def create_pull_request_endpoint(request: CreatePullRequestRequest):
    return create_pull_request_task(
        token=request.github_token,
        repo_owner=request.repo_owner,
        repo_name=request.repo_name,
        username=request.username,
        branch_name=request.branch_name,
        original_branch=request.original_branch,
    )
