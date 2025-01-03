import json

from django.conf import settings
from core.models import Model, WorkflowResult
from tasks.redis_client import RedisStrictClient, RedisVariable

from config.celery import app

redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


@app.task
def save_workflow_result_task(prefix):
    # Embed model
    _, embedding_model_name = Model.get_active_embedding_model()

    # Prompt model
    _, llm_model_name = Model.get_active_llm_model()

    # Embeddings
    embeddings_data = redis_client.get(RedisVariable.EMBEDDINGS, prefix=prefix)
    embeddings = json.loads(embeddings_data) if embeddings_data else None

    # # Context
    context_data = redis_client.get(RedisVariable.CONTEXT, prefix=prefix)
    context = json.loads(context_data) if context_data else None

    # # LLM response
    llm_response = redis_client.get(RedisVariable.LLM_RESPONSE, prefix)

    WorkflowResult.objects.create(
        task_id=prefix,
        embed_model=embedding_model_name,
        prompt_model=llm_model_name,
        embeddings=embeddings,
        context=context,
        llm_response=llm_response,
    )

    return prefix
