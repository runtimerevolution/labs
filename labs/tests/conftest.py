from typing import List

import pytest
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
