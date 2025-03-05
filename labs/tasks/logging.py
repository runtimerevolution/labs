from config.celery import app
from config.redis_client import RedisVariable, redis_client
from core.models import EmbeddingModel, LLMModel, WorkflowResult


@app.task
def save_workflow_result_task(prefix):
    _, embedding_model_name = EmbeddingModel.get_active_model()
    _, llm_model_name = LLMModel.get_active_model()
    project_id = redis_client.get(RedisVariable.PROJECT, prefix)
    embeddings = redis_client.get(RedisVariable.EMBEDDINGS, prefix)
    context = redis_client.get(RedisVariable.CONTEXT, prefix)
    llm_response = redis_client.get(RedisVariable.LLM_RESPONSE, prefix)
    modified_files = redis_client.get(RedisVariable.FILES_MODIFIED, prefix)
    pre_commit_error = redis_client.get(RedisVariable.PRE_COMMIT_ERROR, prefix)

    WorkflowResult.objects.create(
        project_id=project_id,
        task_id=prefix,
        embed_model=embedding_model_name,
        prompt_model=llm_model_name,
        embeddings=embeddings,
        context=context,
        llm_response=llm_response,
        modified_files=modified_files,
        pre_commit_error=pre_commit_error,
    )

    return prefix
