from abc import ABC

from embeddings.embedder import Embedder


class Vectorizer(ABC):
    def __init__(self, vectorizer: type["Vectorizer"], *args, **kwargs):
        if not issubclass(vectorizer, Vectorizer):
            raise TypeError(f"vectorizer must be a subclass of {Vectorizer}")
        self.vectorizer = vectorizer(*args, **kwargs)

    @property
    def embedder(self):
        from core.models import Model  # Avoid circular imports

        embedder_class, *embeder_args = Model.get_active_embedding_model()
        return Embedder(embedder_class, *embeder_args)

    def vectorize_to_database(self, include_file_extensions, repo_destination, *args, **kwargs) -> None:
        self.vectorizer.vectorize_to_database(include_file_extensions, repo_destination, *args, **kwargs)
