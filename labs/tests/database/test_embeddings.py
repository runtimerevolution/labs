import random
from typing import Union

import pytest
from core.models import Project
from embeddings.embedder import Embedder, Embeddings
from embeddings.models import Embedding
from embeddings.openai import OpenAIEmbedder
from core.factories import EmbeddingModelFactory
from tests.constants import MULTIPLE_EMBEDDINGS, OPENAI_EMBEDDING_MODEL_NAME, SINGLE_EMBEDDING


def find_embeddings(project: Union[Project, int]):
    return list(Embedding.objects.filter(project=project))


@pytest.mark.django_db
def test_find_embeddings_no_match():
    result = find_embeddings(1000)

    assert result == []


@pytest.mark.django_db
def test_find_embeddings_one_match(create_single_embedding):
    project, embeddings = create_single_embedding
    result = find_embeddings(project)
    assert result != []

    embedding: Embedding = embeddings[0]
    assert embedding.file_path == SINGLE_EMBEDDING["file_path"]
    assert embedding.text == SINGLE_EMBEDDING["text"]
    assert len(embedding.embedding) == len(SINGLE_EMBEDDING["embedding"])


@pytest.mark.django_db
def test_find_multiple_embeddings(create_multiple_embeddings):
    project, embeddings = create_multiple_embeddings
    assert len(embeddings) == 2

    for i in range(len(embeddings)):
        embedding: Embedding = embeddings[i]
        assert embedding.file_path == MULTIPLE_EMBEDDINGS[i]["file_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert len(embedding.embedding) == len(MULTIPLE_EMBEDDINGS[i]["embedding"])


@pytest.mark.django_db
def test_reembed_code(create_test_project):
    project = create_test_project
    files_texts = [("file1", "text1"), ("file2", "text2")]
    embeddings = Embeddings(
        model="model",
        embeddings=[
            random.sample(range(1, 5000), k=1536),
            random.sample(range(1, 5000), k=1536),
        ],
    )

    embedding_model = EmbeddingModelFactory(
        provider="OPENAI",
        name=OPENAI_EMBEDDING_MODEL_NAME,
        active=True,  
    )

    Embedder(OpenAIEmbedder, model=embedding_model).reembed_code(
        project_id=project.id,
        files_texts=files_texts,
        embeddings=embeddings,
    )

    result = find_embeddings(project)
    assert len(result) == 2

    for i in range(len(result)):
        embedding: Embedding = result[i]
        assert embedding.file_path == MULTIPLE_EMBEDDINGS[i]["file_path"]
        assert embedding.text == MULTIPLE_EMBEDDINGS[i]["text"]
        assert embedding.embedding.size == len(MULTIPLE_EMBEDDINGS[i]["embedding"])
