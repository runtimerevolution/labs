import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from django.conf import settings
from django.db.models import Min
from embeddings.models import Embedding
from pgvector.django import CosineDistance

logger = logging.getLogger(__name__)


@dataclass
class Embeddings:
    model: str
    embeddings: List[Dict[str, Any]]
    model_config: Optional[Dict[str, Any]] = None


class Embedder:
    def __init__(self, embedder, *args, **kwargs):
        self.embedder = embedder(*args, **kwargs)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        return self.embedder.embed(prompt, *args, **kwargs)

    def retrieve_file_paths(
        self,
        query: str,
        repository: str,
        similarity_threshold: float = settings.EMBEDDINGS_SIMILARITY_THRESHOLD,
        max_results: int = settings.EMBEDDINGS_MAX_RESULTS,
    ) -> List[str]:
        query = query.replace("\n", "")
        embedded_query = self.embed(prompt=query).embeddings
        if not embedded_query:
            raise ValueError(f"No embeddings found with the given {query=} with {similarity_threshold=}")

        file_paths = (
            Embedding.objects
            .values("file_path")    # the combination of values and annotate, is the Django way of making a group by
            .annotate(distance=Min(CosineDistance("embedding", embedded_query[0])))
            .order_by("distance")
            .values_list("file_path", flat=True)
        )[:max_results]

        return list(file_paths)

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
