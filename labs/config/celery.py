import logging
import os

import redis
from celery import Celery
from celery.signals import task_failure
from django.conf import settings
from kombu import Queue
from redbeat import RedBeatSchedulerEntry, schedulers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

logger = logging.getLogger(__name__)

CELERY_QUEUE_PREFIX = "code-monkey"
DEFAULT_QUEUE_NAME = CELERY_QUEUE_PREFIX
LOW_PRIORITY_QUEUE_NAME = f"{CELERY_QUEUE_PREFIX}-low"
HIGH_PRIORITY_QUEUE_NAME = f"{CELERY_QUEUE_PREFIX}-high"

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)

app = Celery(
    "config",
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

app.autodiscover_tasks(["tasks"])


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
