from celery import Celery, chain
from celery.signals import task_failure
from kombu import Queue
from redbeat import RedBeatSchedulerEntry, schedulers
import redis
from labs.config import settings
import logging
import json

from labs.database.embeddings import find_similar_embeddings
from labs.database.vectorize_to_db import clone_repository, vectorize_to_db
from labs.middleware import (
    call_agent_to_apply_code_changes,
    get_llm_response,
    get_prompt,
    prepare_context,
)
from run import commit_changes, create_branch, create_pull_request, get_issue


logger = logging.getLogger(__name__)

CELERY_QUEUE_PREFIX = "code-monkey"
DEFAULT_QUEUE_NAME = CELERY_QUEUE_PREFIX
LOW_PRIORITY_QUEUE_NAME = f"{CELERY_QUEUE_PREFIX}-low"
HIGH_PRIORITY_QUEUE_NAME = f"{CELERY_QUEUE_PREFIX}-high"

redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)


app = Celery(
    name="tiktok_connector_worker",
    # If you had tasks defined somewhere other than the name above, you could include them here.
    include=[],
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
    # Consume from queues in original order, so that if the first queue always
    # contains messages, the rest of the queues in the list will never be consumed.
    # This allows priority queues without having to configure many different workers.
    broker_transport_options={"queue_order_strategy": "priority"},
    broker_connection_retry_on_startup=True,
    task_default_queue=DEFAULT_QUEUE_NAME,
    # Queues to consume from. Note that order is important, as it will drain first
    # queue before processing any from the next!
    task_queues=(
        Queue(HIGH_PRIORITY_QUEUE_NAME),
        Queue(DEFAULT_QUEUE_NAME),
        Queue(LOW_PRIORITY_QUEUE_NAME),
    ),
    # Makes sure celery doesn't hijack the root logger and make it so its logs aren't formatted correctly for datadog
    worker_hijack_root_logger=False,
)

# Add a redbeat prefix so that it doesn't mix with other connectors when on a shared cluster.
app.conf.redbeat_key_prefix = CELERY_QUEUE_PREFIX


def get_scheduled_tasks_from_redis():
    redis = schedulers.get_redis(app)
    conf = schedulers.RedBeatConfig(app)
    keys = redis.zrange(conf.schedule_key, 0, -1)
    return [RedBeatSchedulerEntry.from_key(key, app=app) for key in keys]


@task_failure.connect
def notify_slack_task_failure(*args, **kwargs):
    task_id = kwargs.get("task_id", None)
    exception = kwargs.get("exception", None)

    logger.error(f"Task {task_id} has failed. Exception: {exception}")


@app.task(bind=True)
def init_task(self, **kwargs):
    prefix = self.request.id
    for k, v in kwargs.items():
        redis_client.set(f"{prefix}_{k}", v, ex=300)
    return prefix


@app.task
def get_issue_task(prefix="", token="", repo_owner="", repo_name="", issue_number="", username=""):
    token = redis_client.get(f"{prefix}_token") if prefix else token
    repo_owner = redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner
    repo_name = redis_client.get(f"{prefix}_repo_name") if prefix else repo_name
    username = redis_client.get(f"{prefix}_username") if prefix else username
    issue_number = redis_client.get(f"{prefix}_issue_number") if prefix else issue_number

    issue = get_issue(token, repo_owner, repo_name, username, issue_number)

    if prefix:
        issue_title = issue["title"].replace(" ", "-")
        issue_body = issue["body"]
        redis_client.set(f"{prefix}_issue_title", issue_title, ex=300)
        redis_client.set(f"{prefix}_issue_body", issue_body, ex=300)
        return prefix
    return issue


@app.task
def create_branch_task(
    prefix="", token="", repo_owner="", repo_name="", issue_number="", username="", original_branch="", issue_title=""
):
    token = redis_client.get(f"{prefix}_token") if prefix else token
    repo_owner = redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner
    repo_name = redis_client.get(f"{prefix}_repo_name") if prefix else repo_name
    username = redis_client.get(f"{prefix}_username") if prefix else username
    issue_number = redis_client.get(f"{prefix}_issue_number") if prefix else issue_number
    original_branch = redis_client.get(f"{prefix}_original_branch") if prefix else original_branch
    issue_title = redis_client.get("issue_title") if prefix else issue_title

    branch_name = create_branch(token, repo_owner, repo_name, username, issue_number, original_branch, issue_title)

    if prefix:
        redis_client.set(f"{prefix}_branch_name", branch_name, ex=300)
        return prefix
    return branch_name


@app.task
def clone_repo_task(prefix="", repo_owner="", repo_name=""):
    repo_owner = redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner
    repo_name = redis_client.get(f"{prefix}_repo_name") if prefix else repo_name
    repo_destination = f"{settings.CLONE_DESTINATION_DIR}{repo_owner}/{repo_name}"
    clone_repository(f"https://github.com/{repo_owner}/{repo_name}", repo_destination)

    if prefix:
        redis_client.set(f"{prefix}_repo_destination", repo_destination, ex=300)
        return prefix
    return True


@app.task
def vectorize_repo_to_database_task(prefix="", repo_destination=""):
    repo_destination = redis_client.get(f"{prefix}_repo_destination") if prefix else repo_destination
    vectorize_to_db(None, repo_destination)

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

    embeddings = json.loads(redis_client.get(f"{prefix}_similar_embeddings") if prefix else embeddings)
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


@app.task
def apply_code_changes_task(prefix="", llm_response=""):
    llm_response = redis_client.get(f"{prefix}_llm_response") if prefix else llm_response
    files_modified = call_agent_to_apply_code_changes(llm_response)

    if prefix:
        redis_client.set(f"{prefix}_files_modified", json.dumps(files_modified))
        return prefix
    return files_modified


@app.task
def commit_changes_task(
    prefix="", token="", repo_owner="", repo_name="", username="", branch_name="", files_modified=[]
):
    commit_changes(
        token=redis_client.get(f"{prefix}_token") if prefix else token,
        repo_owner=redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner,
        repo_name=redis_client.get(f"{prefix}_repo_name") if prefix else repo_name,
        username=redis_client.get(f"{prefix}_username") if prefix else username,
        branch_name=redis_client.get(f"{prefix}_branch_name") if prefix else branch_name,
        file_list=json.loads(redis_client.get(f"{prefix}_files_modified")) if prefix else files_modified,
    )

    if prefix:
        return prefix
    return True


@app.task
def create_pull_request_task(
    prefix="", token="", repo_owner="", repo_name="", username="", branch_name="", original_branch=""
):
    create_pull_request(
        token=redis_client.get(f"{prefix}_token") if prefix else token,
        repo_owner=redis_client.get(f"{prefix}_repo_owner") if prefix else repo_owner,
        repo_name=redis_client.get(f"{prefix}_repo_name") if prefix else repo_name,
        username=redis_client.get(f"{prefix}_username") if prefix else username,
        original_branch=redis_client.get(f"{prefix}_original_branch") if prefix else original_branch,
        branch_name=redis_client.get(f"{prefix}_branch_name") if prefix else branch_name,
    )

    if prefix:
        return prefix
    return True


@app.task
def run_on_repo_task(
    token: str,
    repo_owner: str,
    repo_name: str,
    username: str,
    issue_number: int,
    original_branch: str = "main",
):
    data = {
        "token": token,
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "username": username,
        "issue_number": issue_number,
        "original_branch": original_branch,
    }
    chain(
        init_task.s(**data),
        get_issue_task.s(),
        create_branch_task.s(),
        clone_repo_task.s(),
        vectorize_repo_to_database_task.s(),
        find_similar_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
        commit_changes_task.s(),
        create_pull_request_task.s(),
    ).apply_async()


@app.task
def run_on_local_repo_task(repo_path, issue_text):
    data = {
        "repo_path": repo_path,
        "issue_text": issue_text,
        "issue_body": issue_text,
        "repo_destination": repo_path,
    }
    chain(
        init_task.s(**data),
        vectorize_repo_to_database_task.s(),
        find_similar_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
    ).apply_async()
