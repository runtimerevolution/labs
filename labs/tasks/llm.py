import json
import logging

import config.configuration_variables as settings
from config.celery import app
from core.models import Model, VectorizerModel
from embeddings.embedder import Embedder
from embeddings.vectorizers.vectorizer import Vectorizer
from llm.requester import Requester
from tasks.checks import run_response_checks
from tasks.redis_client import RedisStrictClient, RedisVariables

logger = logging.getLogger(__name__)
redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


def get_prompt(issue_summary):
    return f"""
        You're a diligent software engineer AI. You can't see, draw, or interact with a 
        browser, but you can read and write files, and you can think.
        You've been given the following task: {issue_summary}.
        Any imports will be at the beggining of the file.
        Add tests for the new functionalities, considering any existing test files.
        The file paths provided are **absolute paths relative to the project root**, 
        and **must not be changed**. Ensure the paths you output match the paths provided exactly. 
        Do not prepend or modify the paths.
        Please provide a json response in the following format: {{"steps": [...]}}
        Where steps is a list of objects where each object contains three fields:
        type, which is either 'create' to add a new file or 'modify' to edit an existing one;
        If the file is to be modified send the finished version of the entire file.
        path, which is the absolute path of the file to create/modify;
        content, which is the content to write to the file.
    """


def get_context(embeddings, prompt):
    context = []
    for file in embeddings:
        context.append(dict(role="system", content=f"File: {file[1]}, Content: {file[2]}"))

    context.append(dict(role="user", content=prompt))
    return context


def get_llm_response(prompt):
    llm_requester, *llm_requester_args = Model.get_active_llm_model()
    requester = Requester(llm_requester, *llm_requester_args)

    retries, max_retries = 0, 5
    is_invalid, reason = True, None

    llm_response = None
    while is_invalid and retries < max_retries:
        try:
            llm_response = requester.completion_without_proxy(prompt)
            logger.debug(f"LLM reponse: {llm_response}")

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
    repository_path = redis_client.get(RedisVariables.REPOSITORY_PATH, prefix=prefix, default=repository_path)

    embedder_class, *embeder_args = Model.get_active_embedding_model()
    embedder = Embedder(embedder_class, *embeder_args)

    vectorizer_class = VectorizerModel.get_active_vectorizer()
    Vectorizer(vectorizer_class, embedder).vectorize_to_database(None, repository_path)

    if prefix:
        return prefix
    return True


@app.task
def find_embeddings_task(prefix="", issue_body="", repository_path=""):
    embedder_class, *embeder_args = Model.get_active_embedding_model()
    embeddings_results = Embedder(embedder_class, *embeder_args).retrieve_embeddings(
        redis_client.get(RedisVariables.ISSUE_BODY, prefix=prefix, default=issue_body),
        redis_client.get(RedisVariables.REPOSITORY_PATH, prefix=prefix, default=repository_path),
    )
    similar_embeddings = [
        (embedding.repository, embedding.file_path, embedding.text) for embedding in embeddings_results
    ]

    if prefix:
        redis_client.set(RedisVariables.EMBEDDINGS, prefix=prefix, value=json.dumps(similar_embeddings))
        return prefix
    return similar_embeddings


@app.task
def prepare_prompt_and_context_task(prefix="", issue_body="", embeddings=[]):
    prompt = get_prompt(redis_client.get(RedisVariables.ISSUE_BODY, prefix=prefix, default=issue_body))
    redis_client.set(RedisVariables.PROMPT, prefix=prefix, value=prompt)

    embeddings = json.loads(redis_client.get(RedisVariables.EMBEDDINGS, prefix=prefix, default=embeddings))
    prepared_context = get_context(embeddings, prompt)

    if prefix:
        redis_client.set(RedisVariables.CONTEXT, prefix=prefix, value=json.dumps(prepared_context))
        return prefix
    return prepared_context


@app.task
def get_llm_response_task(prefix="", context={}):
    context = json.loads(redis_client.get(RedisVariables.CONTEXT, prefix=prefix, default=context))
    llm_response = get_llm_response(context)

    if prefix:
        redis_client.set(
            RedisVariables.LLM_RESPONSE,
            prefix=prefix,
            value=llm_response[1][1]["choices"][0]["message"]["content"],
        )
        return prefix
    return llm_response
