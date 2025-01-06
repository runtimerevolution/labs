from django.conf import settings
from core.models import Model, WorkflowResult
from config.redis_client import RedisStrictClient, RedisVariable

from config.celery import app

redis_client = RedisStrictClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)


@app.task
def save_workflow_result_task(prefix):
    # Embed model
    _, embedding_model_name = Model.get_active_embedding_model()

    # Prompt model
    _, llm_model_name = Model.get_active_llm_model()

    # Embeddings
    embeddings = redis_client.get(RedisVariable.EMBEDDINGS, prefix=prefix)

    # Context
    context = redis_client.get(RedisVariable.CONTEXT, prefix=prefix)

    # LLM response
    llm_response = redis_client.get(RedisVariable.LLM_RESPONSE, prefix)

    # Modified files
    modified_files = redis_client.get(RedisVariable.FILES_MODIFIED, prefix)

    WorkflowResult.objects.create(
        task_id=prefix,
        embed_model=embedding_model_name,
        prompt_model=llm_model_name,
        embeddings=embeddings,
        context=context,
        llm_response=llm_response,
        modified_files=modified_files,
    )

    return prefix
