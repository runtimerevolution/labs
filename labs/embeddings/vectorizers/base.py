from abc import ABC

from embeddings.embedder import Embedder


class Vectorizer:
    def __init__(self, vectorizer, *args, **kwargs):
        self.vectorizer = vectorizer(*args, **kwargs)

    def vectorize_to_database(self, include_file_extensions, repo_destination, *args, **kwargs) -> None:
        self.vectorizer.vectorize_to_database(include_file_extensions, repo_destination, *args, **kwargs)
