import pytest
from rag import find_similar_embeddings

def test_find_similar_embeddings():
    query = "This is a sample query."
    result = find_similar_embeddings(query)
    assert result is not None, "Similar embeddings not found."