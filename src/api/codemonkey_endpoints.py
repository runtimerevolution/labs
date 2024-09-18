from fastapi import APIRouter, HTTPException
from run import call_llm_with_context, run
from src.api.types import CallLLMRequest, CodeMonkeyRequest, GithubModel
from src.config.settings import LITELLM_API_KEY

router = APIRouter()


@router.post("/codemonkey/run")
async def list_issues(request: CodeMonkeyRequest):
    try:
        return run(request=request)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.post("/codemonkey/llm_with_context")
async def llm_with_context(github: GithubModel, params: CallLLMRequest):
    try:
        outputted_files = call_llm_with_context(
            github, params.issue_summary, litellm_api_key=LITELLM_API_KEY
        )
        return outputted_files

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
