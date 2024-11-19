from typing import List

import pytest
from core.models import Model
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
    config = Model.objects.create(
        model_type="EMBEDDING", provider="OLLAMA", model_name=OLLAMA_EMBEDDING_MODEL_NAME, active=True
    )
    return config


@pytest.fixture
@pytest.mark.django_db
def create_test_ollama_llm_config():
    config = Model.objects.create(model_type="LLM", provider="OLLAMA", model_name=OLLAMA_LLM_MODEL_NAME, active=True)
    return config


@pytest.fixture
@pytest.mark.django_db
def create_test_openai_embedding_config():
    config = Model.objects.create(
        model_type="EMBEDDING", provider="OPENAI", model_name=OPENAI_EMBEDDING_MODEL_NAME, active=True
    )
    return config


@pytest.fixture
@pytest.mark.django_db
def create_test_openai_llm_config():
    config = Model.objects.create(model_type="LLM", provider="OPENAI", model_name=OPENAI_LLM_MODEL_NAME, active=True)
    return config
