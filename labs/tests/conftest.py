from typing import List

import pytest
from core.models import Config
from embeddings.models import Embedding
from tests.constants import MULTIPLE_EMBEDDINGS, SINGLE_EMBEDDING


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
def create_test_embedding_config():
    config = Config.objects.create(
        model_type="EMBEDDING", provider="OLLAMA", model_name="nomic-embed-text:latest", active=True
    )
    return config


@pytest.fixture
@pytest.mark.django_db
def create_test_llm_config():
    config = Config.objects.create(model_type="LLM", provider="OLLAMA", model_name="llama3.2:latest", active=True)
    return config
