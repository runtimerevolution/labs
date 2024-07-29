
from rag import find_similar_embeddings
import pytest

  query = "This is a sample query."
  def test_find_similar_embeddings():
      result = find_similar_embeddings(query)
      assert result is not None, "Similar embeddings not found."