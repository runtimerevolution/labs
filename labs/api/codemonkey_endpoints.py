from fastapi import APIRouter, HTTPException
from labs.api.types import CallLLMRequest, CodeMonkeyRequest, GithubModel
from labs.config.settings import LITELLM_API_KEY
from labs.decorators import async_time_and_log_function
from run import call_llm_with_context, run
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/codemonkey/run")
@async_time_and_log_function
async def codemonkey_run(request: CodeMonkeyRequest):
    try:
        return run(request=request)
    except Exception as e:
        logger.exception("Internal server error")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.post("/codemonkey/llm_with_context")
@async_time_and_log_function
async def llm_with_context(github: GithubModel, params: CallLLMRequest):
    try:
        outputted_files = call_llm_with_context(
            github, params.issue_summary, litellm_api_key=LITELLM_API_KEY
        )
        return outputted_files

    except Exception as e:
        logger.exception("Internal server error")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
