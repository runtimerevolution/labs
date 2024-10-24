import redis
from config import configuration_variables as settings
import logging
import json

from labs.database.embeddings import find_similar_embeddings
from labs.database.vectorize.chunk_vectorizer import ChunkVectorizer
from labs.llm import get_llm_response, get_prompt, prepare_context
from labs.celery import app


logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


@app.task
def vectorize_repo_to_database_task(prefix="", repo_destination=""):
    repo_destination = redis_client.get(f"{prefix}_repo_destination") if prefix else repo_destination
    ChunkVectorizer().vectorize_to_database(None, repo_destination)

    if prefix:
        return prefix
    return True


@app.task
def find_similar_embeddings_task(prefix="", issue_body=""):
    rows = find_similar_embeddings(redis_client.get(f"{prefix}_issue_body") if prefix else issue_body)
    similar_embeddings = [(row[0], row[1], row[2]) for row in rows]

    if prefix:
        redis_client.set(f"{prefix}_similar_embeddings", json.dumps(similar_embeddings))
        return prefix
    return similar_embeddings


@app.task
def prepare_prompt_and_context_task(prefix="", issue_body="", embeddings=[]):
    prompt = get_prompt(redis_client.get(f"{prefix}_issue_body") if prefix else issue_body)
    redis_client.set(f"{prefix}_prompt", prompt)

    embeddings = json.loads(redis_client.get(f"{prefix}_similar_embeddings")) if prefix else embeddings
    prepared_context = prepare_context(embeddings, prompt)

    if prefix:
        redis_client.set(f"{prefix}_prepared_context", json.dumps(prepared_context))
        return prefix
    return prepared_context


@app.task
def get_llm_response_task(prefix="", context={}):
    context = json.loads(redis_client.get(f"{prefix}_prepared_context")) if prefix else context
    llm_response = get_llm_response(context)

    if prefix:
        redis_client.set(f"{prefix}_llm_response", llm_response[1][1].choices[0].message.content)
        return prefix
    return llm_response
