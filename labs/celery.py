from celery import Celery, chain
from celery.signals import task_failure
from kombu import Queue
from redbeat import RedBeatSchedulerEntry, schedulers
import redis
from labs.api.types import CodeMonkeyRequest
from labs.config import settings
import logging
import json

from labs.database.embeddings import find_similar_embeddings
from labs.database.vectorize_to_db import vectorize_to_db
from labs.github.github import GithubRequests
from labs.middleware import (
    call_agent_to_apply_code_changes,
    get_llm_response,
    get_prompt,
    prepare_context,
)
from run import Run


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
def init_task(
    self,
    token: str,
    repo_owner: str,
    repo_name: str,
    username: str,
    issue_number: int,
    original_branch: str = "",
):
    prefix = self.request.id
    redis_client.set(f"{prefix}_token", token, ex=300)
    redis_client.set(f"{prefix}_repo_owner", repo_owner, ex=300)
    redis_client.set(f"{prefix}_repo_name", repo_name, ex=300)
    redis_client.set(f"{prefix}_username", username, ex=300)
    redis_client.set(f"{prefix}_issue_number", issue_number, ex=300)
    redis_client.set(f"{prefix}_original_branch", original_branch, ex=300)
    return prefix


@app.task
def get_issue_task(prefix: str):
    request = CodeMonkeyRequest(
        github_token=redis_client.get(f"{prefix}_token"),
        repo_owner=redis_client.get(f"{prefix}_repo_owner"),
        repo_name=redis_client.get(f"{prefix}_repo_name"),
        username=redis_client.get(f"{prefix}_username"),
        issue_number=redis_client.get(f"{prefix}_issue_number"),
    )
    issue = Run(request).get_issue()
    issue_title = issue["title"].replace(" ", "-")
    redis_client.set(f"{prefix}_issue_title", issue_title, ex=300)
    issue_body = issue["body"]
    redis_client.set(f"{prefix}_issue_body", issue_body, ex=300)
    return prefix


@app.task
def create_branch_task(prefix: str):
    request = CodeMonkeyRequest(
        github_token=redis_client.get(f"{prefix}_token"),
        repo_owner=redis_client.get(f"{prefix}_repo_owner"),
        repo_name=redis_client.get(f"{prefix}_repo_name"),
        username=redis_client.get(f"{prefix}_username"),
        issue_number=redis_client.get(f"{prefix}_issue_number"),
        original_branch=redis_client.get(f"{prefix}_original_branch"),
    )
    branch_name = Run(request).create_branch(redis_client.get("issue_title"))
    redis_client.set(f"{prefix}_branch_name", branch_name, ex=300)
    return prefix


@app.task
def vectorize_to_database_task(prefix: str):
    repo_owner = redis_client.get(f"{prefix}_repo_owner")
    repo_name = redis_client.get(f"{prefix}_repo_name")
    destination = f"{settings.CLONE_DESTINATION_DIR}{repo_owner}/{repo_name}"
    vectorize_to_db(f"https://github.com/{repo_owner}/{repo_name}", None, destination)
    return prefix


@app.task
def find_similar_embeddings_task(prefix: str):
    rows = find_similar_embeddings(redis_client.get(f"{prefix}_issue_body"))
    similar_embeddings = [(row[0], row[1], row[2]) for row in rows]
    json_similar_embeddings = json.dumps(similar_embeddings)
    redis_client.set(f"{prefix}_similar_embeddings", json_similar_embeddings)
    return prefix


@app.task
def prepare_prompt_and_context_task(prefix: str):
    prompt = get_prompt(redis_client.get(f"{prefix}_issue_body"))
    redis_client.set(f"{prefix}_prompt", prompt)

    similar_embeddings = json.loads(redis_client.get(f"{prefix}_similar_embeddings"))
    prepared_context = prepare_context(similar_embeddings, prompt)
    json_prepared_context = json.dumps(prepared_context)
    redis_client.set(f"{prefix}_prepared_context", json_prepared_context)

    return prefix


@app.task
def get_llm_response_task(prefix: str):
    prepared_context = json.loads(redis_client.get(f"{prefix}_prepared_context"))
    llm_response = get_llm_response(prepared_context)
    redis_client.set(
        f"{prefix}_llm_response", llm_response[1][1].choices[0].message.content
    )
    return prefix


@app.task
def apply_code_changes_task(prefix: str):
    llm_response = redis_client.get(f"{prefix}_llm_response")
    files_modified = call_agent_to_apply_code_changes(llm_response)
    redis_client.set(f"{prefix}_files_modified", json.dumps(files_modified))
    return prefix


@app.task
def commit_changes_task(prefix: str):
    github_request = GithubRequests(
        github_token=redis_client.get(f"{prefix}_token"),
        repo_owner=redis_client.get(f"{prefix}_repo_owner"),
        repo_name=redis_client.get(f"{prefix}_repo_name"),
        username=redis_client.get(f"{prefix}_username"),
    )

    branch_name = redis_client.get(f"{prefix}_branch_name")
    files_modified = json.loads(redis_client.get(f"{prefix}_files_modified"))
    github_request.commit_changes("fix", branch_name=branch_name, files=files_modified)
    return prefix


@app.task
def create_pull_request_task(prefix: str):
    github_request = GithubRequests(
        github_token=redis_client.get(f"{prefix}_token"),
        repo_owner=redis_client.get(f"{prefix}_repo_owner"),
        repo_name=redis_client.get(f"{prefix}_repo_name"),
        username=redis_client.get(f"{prefix}_username"),
    )

    branch_name = redis_client.get(f"{prefix}_branch_name")
    original_branch = redis_client.get(f"{prefix}_original_branch")
    github_request.create_pull_request(branch_name, base=original_branch)
    return prefix


@app.task
def run_task(
    token: str,
    repo_owner: str,
    repo_name: str,
    username: str,
    issue_number: int,
    original_branch: str,
):
    chain(
        init_task.s(
            token, repo_owner, repo_name, username, issue_number, original_branch
        ),
        get_issue_task.s(),
        create_branch_task.s(),
        vectorize_to_database_task.s(),
        find_similar_embeddings_task.s(),
        prepare_prompt_and_context_task.s(),
        get_llm_response_task.s(),
        apply_code_changes_task.s(),
        commit_changes_task.s(),
        create_pull_request_task.s(),
    ).apply_async()
