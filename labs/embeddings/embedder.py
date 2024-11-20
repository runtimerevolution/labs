from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from embeddings.models import Embedding
from pgvector.django import CosineDistance


@dataclass
class Embeddings:
    model: str
    embeddings: List[Dict[str, Any]]
    model_config: Optional[Dict[str, Any]] = None


class Embedder(ABC):
    def __init__(self, embedder, *args, **kwargs):
        self.embedder = embedder(*args, **kwargs)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        return self.embedder.embed(prompt, *args, **kwargs)

    def retrieve_embeddings(
        self, query: str, similarity_threshold: int = 0.7, number_of_results: int = 10
    ) -> List[Embeddings]:
        query = query.replace("\n", "")
        embedded_query = self.embed(prompt=query).embeddings[0]

        return Embedding.objects.annotate(distance=CosineDistance("embedding", embedded_query)).filter(
            distance__lt=similarity_threshold
        )[:number_of_results]

    def reembed_code(
        self,
        repository: str,
        files_texts: Union[str, List[str]],
        embeddings: Any = None,
    ) -> None:
        Embedding.objects.filter(repository=repository).delete()

        if not embeddings:
            embeddings = self.embed(prompt=files_texts)

        for file_text, file_text_embedding in zip(files_texts, embeddings.embeddings):
            Embedding.objects.create(
                repository=repository,
                embedding=file_text_embedding,
                file_path=file_text[0],
                text=file_text[1],
            )
