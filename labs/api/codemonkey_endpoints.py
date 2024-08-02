from fastapi import APIRouter
from labs.api.types import CallLLMRequest, CodeMonkeyRequest, GithubModel
from labs.config import LITELLM_API_KEY
from run import call_llm_with_context, run

router = APIRouter()


@router.post("/codemonkey/run")
async def list_issues(request: CodeMonkeyRequest):

    return run(request=request)


@router.post("/codemonkey/llm_with_context")
async def llm_with_context(github: GithubModel, params: CallLLMRequest):
    outputted_files = call_llm_with_context(
        github, params.issue_summary, litellm_api_key=LITELLM_API_KEY
    )
    return outputted_files
