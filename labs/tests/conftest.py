from typing import List

import pytest
from core.models import Model, ModelTypeEnum, Project, ProviderEnum, Variable
from embeddings.models import Embedding
from tests.constants import (
    ANTHROPIC_LLM_MODEL_NAME,
    GEMINI_EMBEDDING_MODEL_NAME,
    GEMINI_LLM_MODEL_NAME,
    MULTIPLE_EMBEDDINGS,
    OLLAMA_EMBEDDING_MODEL_NAME,
    OLLAMA_LLM_MODEL_NAME,
    OPENAI_EMBEDDING_MODEL_NAME,
    OPENAI_LLM_MODEL_NAME,
    SINGLE_EMBEDDING,
)


@pytest.fixture
@pytest.mark.django_db()
def create_test_project():
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_VECTORIZER", value="CHUNK_VECTORIZER")
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_PERSONA", value="persona")
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_INSTRUCTION", value="instruction")
    return Project.objects.create(name="test", path="project_path")


@pytest.fixture
@pytest.mark.django_db
def create_single_embedding(create_test_project):
    project = create_test_project
    embedding = Embedding.objects.create(project=project, **SINGLE_EMBEDDING)

    return project, [embedding]


@pytest.fixture
@pytest.mark.django_db
def create_multiple_embeddings(create_test_project):
    project = create_test_project

    embeddings: List[Embedding] = []
    for embedding_params in MULTIPLE_EMBEDDINGS:
        embeddings.append(Embedding(project=project, **embedding_params))

    Embedding.objects.bulk_create(embeddings)
    return project, embeddings


@pytest.fixture
@pytest.mark.django_db
def create_test_ollama_embedding_config():
    return Model.objects.create(
        model_type=ModelTypeEnum.EMBEDDING.name,
        provider=ProviderEnum.OLLAMA.name,
        model_name=OLLAMA_EMBEDDING_MODEL_NAME,
        active=True,
    )


@pytest.fixture
@pytest.mark.django_db
def create_test_ollama_llm_config():
    return Model.objects.create(
        model_type=ModelTypeEnum.LLM.name,
        provider=ProviderEnum.OLLAMA.name,
        model_name=OLLAMA_LLM_MODEL_NAME,
        active=True,
    )


@pytest.fixture
@pytest.mark.django_db
def create_test_openai_embedding_config():
    return Model.objects.create(
        model_type=ModelTypeEnum.EMBEDDING.name,
        provider=ProviderEnum.OPENAI.name,
        model_name=OPENAI_EMBEDDING_MODEL_NAME,
        active=True,
    )


@pytest.fixture
@pytest.mark.django_db
def create_test_openai_llm_config():
    return Model.objects.create(
        model_type=ModelTypeEnum.LLM.name,
        provider=ProviderEnum.OPENAI.name,
        model_name=OPENAI_LLM_MODEL_NAME,
        active=True,
    )


@pytest.fixture
@pytest.mark.django_db
def create_test_gemini_embedding_config():
    return Model.objects.create(
        model_type=ModelTypeEnum.EMBEDDING.name,
        provider=ProviderEnum.GEMINI.name,
        model_name=GEMINI_EMBEDDING_MODEL_NAME,
        active=True,
    )


@pytest.fixture
@pytest.mark.django_db
def create_test_gemini_llm_config():
    return Model.objects.create(
        model_type=ModelTypeEnum.LLM.name,
        provider=ProviderEnum.GEMINI.name,
        model_name=GEMINI_LLM_MODEL_NAME,
        active=True,
    )


@pytest.fixture
@pytest.mark.django_db
def create_test_anthropic_llm_config():
    return Model.objects.create(
        model_type=ModelTypeEnum.LLM.name,
        provider=ProviderEnum.ANTHROPIC.name,
        model_name=ANTHROPIC_LLM_MODEL_NAME,
        active=True,
    )
