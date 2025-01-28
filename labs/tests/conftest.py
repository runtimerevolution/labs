from typing import List

import pytest
from core.models import Model, ModelTypeEnum, Project, ProviderEnum, Variable, VectorizerEnum, VectorizerModel
from embeddings.models import Embedding
from tests.constants import (
    MULTIPLE_EMBEDDINGS,
    OLLAMA_EMBEDDING_MODEL_NAME,
    OLLAMA_LLM_MODEL_NAME,
    OPENAI_EMBEDDING_MODEL_NAME,
    OPENAI_LLM_MODEL_NAME,
    SINGLE_EMBEDDING,
)


@pytest.fixture
@pytest.mark.django_db
def create_test_embedding():
    embedding = Embedding(**SINGLE_EMBEDDING)
    embedding.save()

    return [embedding]


@pytest.fixture
@pytest.mark.django_db
def create_test_embeddings():
    embeddings: List[Embedding] = []

    for embedding in MULTIPLE_EMBEDDINGS:
        embeddings.append(Embedding(**embedding))

    Embedding.objects.bulk_create(embeddings)
    return embeddings


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
def create_test_chunk_vectorizer_config():
    return VectorizerModel.objects.create(vectorizer_type=VectorizerEnum.CHUNK_VECTORIZER.name)


@pytest.fixture
@pytest.mark.django_db
def create_test_project():
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_VECTORIZER", value="CHUNK_VECTORIZER")
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_PERSONA", value="persona")
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_INSTRUCTION", value="instruction")
    return Project.objects.create(name="test", path="repository_path")
