import json
import logging
from typing import List, Optional

from config.celery import app
from config.redis_client import RedisVariable, redis_client
from core.models import Model, VectorizerModel
from django.conf import settings
from embeddings.embedder import Embedder
from embeddings.vectorizers.vectorizer import Vectorizer
from llm.checks import run_response_checks
from llm.context import get_context
from llm.prompt import get_prompt
from llm.requester import Requester

logger = logging.getLogger(__name__)


def get_llm_response(prompt):
    llm_requester, *llm_requester_args = Model.get_active_llm_model()
    requester = Requester(llm_requester, *llm_requester_args)

    retries, max_retries = 0, 5
    is_invalid, reason = True, None

    llm_response = None
    while is_invalid and retries < max_retries:
        try:
            llm_response = requester.completion_without_proxy(prompt)
            logger.debug(f"LLM response: {llm_response}")

            is_invalid, reason = run_response_checks(llm_response)

        except Exception as e:
            is_invalid, reason = True, str(e)
            logger.error("Invalid LLM response:", exc_info=e)

        if is_invalid:
            retries += 1
            llm_response = None
            logger.info(f"Redoing LLM response request doe to error (retries: {retries} of {max_retries}): {reason}")

    return True, llm_response


@app.task
def vectorize_repository_task(prefix="", repository_path=""):
    repository_path = redis_client.get(RedisVariable.REPOSITORY_PATH, prefix=prefix, default=repository_path)

    embedder_class, *embeder_args = Model.get_active_embedding_model()
    embedder = Embedder(embedder_class, *embeder_args)

    vectorizer_class = VectorizerModel.get_active_vectorizer()
    Vectorizer(vectorizer_class, embedder).vectorize_to_database(None, repository_path)

    if prefix:
        return prefix
    return True


@app.task
def find_embeddings_task(
    prefix="",
    issue_body="",
    repository_path="",
    similarity_threshold=settings.EMBEDDINGS_SIMILARITY_THRESHOLD,
    max_results=settings.EMBEDDINGS_MAX_RESULTS,
):
    embedder_class, *embeder_args = Model.get_active_embedding_model()
    files_path = Embedder(embedder_class, *embeder_args).retrieve_files_path(
        redis_client.get(RedisVariable.ISSUE_BODY, prefix=prefix, default=issue_body),
        redis_client.get(RedisVariable.REPOSITORY_PATH, prefix=prefix, default=repository_path),
        similarity_threshold,
        max_results,
    )
    logger.debug(f"Retrieved files from embeddings match\n: {'\n'.join(files_path)}")

    if prefix:
        redis_client.set(RedisVariable.EMBEDDINGS, prefix=prefix, value=json.dumps(files_path))
        return prefix
    return files_path


@app.task
def prepare_prompt_and_context_task(prefix="", issue_body="", embeddings: Optional[List[str]] = None):
    if not embeddings:
        embeddings = []

    prompt = get_prompt(redis_client.get(RedisVariable.ISSUE_BODY, prefix=prefix, default=issue_body))
    redis_client.set(RedisVariable.PROMPT, prefix=prefix, value=prompt)

    embeddings = json.loads(redis_client.get(RedisVariable.EMBEDDINGS, prefix=prefix, default=embeddings))
    prepared_context = get_context(embeddings, prompt)

    if prefix:
        redis_client.set(RedisVariable.CONTEXT, prefix=prefix, value=json.dumps(prepared_context))
        return prefix
    return prepared_context


@app.task
def get_llm_response_task(prefix="", context=None):
    if not context:
        context = {}

    context = json.loads(redis_client.get(RedisVariable.CONTEXT, prefix=prefix, default=context))
    llm_response = get_llm_response(context)

    if prefix:
        redis_client.set(
            RedisVariable.LLM_RESPONSE,
            prefix=prefix,
            value=llm_response[1][1]["choices"][0]["message"]["content"],
        )
        return prefix
    return llm_response
