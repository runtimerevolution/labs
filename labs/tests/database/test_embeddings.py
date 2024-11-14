import random

import pytest
from embeddings.base import Embedder, Embeddings
from embeddings.models import Embedding
from embeddings.openai import OpenAIEmbedder
from tests.constants import MULTIPLE_EMBEDDINGS, REPO1, SINGLE_EMBEDDING


def find_embeddings(repository: str):
    return list(Embedding.objects.filter(repository=repository))


@pytest.mark.django_db
def test_find_embeddings_no_match():
    result = find_embeddings("")

    assert result == []


@pytest.mark.django_db
def test_find_embeddings_one_match(create_test_embedding):
    result = find_embeddings(REPO1)
    assert result != []

    embedding: Embedding = result[0]
    assert embedding.file_path == SINGLE_EMBEDDING["file_path"]
    assert embedding.text == SINGLE_EMBEDDING["text"]
    assert embedding.embedding.size == len(SINGLE_EMBEDDING["embedding"])


@pytest.mark.django_db
def test_find_multiple_embeddings(create_test_embeddings):
    result = find_embeddings(REPO1)
    assert len(result) == 2

    for i in range(len(result)):
        embedding: Embedding = result[i]
        assert embedding.file_path == MULTIPLE_EMBEDDINGS[i]["file_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert embedding.embedding.size == len(MULTIPLE_EMBEDDINGS[i]["embedding"])


@pytest.mark.django_db
def test_reembed_code():
    files_texts = [("file1", "text1"), ("file2", "text2")]
    embeddings = Embeddings(
        model="model",
        embeddings=[
            random.sample(range(1, 5000), k=1536),
            random.sample(range(1, 5000), k=1536),
        ],
    )

    Embedder(OpenAIEmbedder).reembed_code(
        files_texts=files_texts,
        embeddings=embeddings,
        repository=REPO1,
    )

    result = find_embeddings(REPO1)
    assert len(result) == 2

    for i in range(len(result)):
        embedding: Embedding = result[i]
        assert embedding.file_path == MULTIPLE_EMBEDDINGS[i]["file_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert embedding.embedding.size == len(MULTIPLE_EMBEDDINGS[i]["embedding"])
