from core.models import Model, WorkflowResult

from config.celery import app
from config.redis_client import RedisVariable, redis_client


@app.task
def save_workflow_result_task(prefix):
    _, embedding_model_name = Model.get_active_embedding_model()
    _, llm_model_name = Model.get_active_llm_model()
    embeddings = redis_client.get(RedisVariable.EMBEDDINGS, prefix=prefix)
    context = redis_client.get(RedisVariable.CONTEXT, prefix=prefix)
    llm_response = redis_client.get(RedisVariable.LLM_RESPONSE, prefix)
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
