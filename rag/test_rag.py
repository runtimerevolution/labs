import pytest
from rag import find_similar_embeddings

def test_find_similar_embeddings_with_existing_data():
    query = "This is a sample query."
    result = find_similar_embeddings(query)
    assert result is not None, "Similar embeddings not found."

def test_find_similar_embeddings_with_no_data():
    query = "Further testing of similar embeddings."
    result = find_similar_embeddings(query)
    assert result is not None, "Similar embeddings not found."
     
def test_find_similar_embeddings_empty_query():
    query = ""
    result = find_similar_embeddings(query)
    assert result is not None, "Similar embeddings not found."

def test_find_similar_embeddings_multi_line_query():
    query = "This is a multi-line \n query with special characters !@#$%^&"
    result = find_similar_embeddings(query)
    assert result is not None, "Similar embeddings not found."