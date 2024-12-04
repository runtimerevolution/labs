import json

import config.configuration_variables as settings
from config.celery import app
from core.models import Model, VectorizerModel
from embeddings.embedder import Embedder
from embeddings.vectorizers.base import Vectorizer
from llm import get_llm_response, get_prompt, prepare_context
from tasks.redis_client import RedisStrictClient, RedisVariables

redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


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
    prepared_context = prepare_context(embeddings, prompt)

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
