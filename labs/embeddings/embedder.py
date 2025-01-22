from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from django.conf import settings
from django.db.models import Min
from embeddings.models import Embedding
from pgvector.django import CosineDistance

logger = logging.getLogger(__name__)


# Avoid importing circulars due to typing
if TYPE_CHECKING:
    from core.models import Project


@dataclass
class Embeddings:
    model: str
    embeddings: Union[List[Dict[str, Any]], List[List[int]]]
    model_config: Optional[Dict[str, Any]] = None


class Embedder:
    def __init__(self, embedder, *args, **kwargs):
        self.embedder = embedder(*args, **kwargs)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        return self.embedder.embed(prompt, *args, **kwargs)

    def retrieve_files_path(
        self,
        query: str,
        project: Project,
        similarity_threshold: float = settings.EMBEDDINGS_SIMILARITY_THRESHOLD,
        max_results: int = settings.EMBEDDINGS_MAX_RESULTS,
    ) -> List[str]:
        query = query.replace("\n", "")
        embedded_query = self.embed(prompt=query).embeddings
        if not embedded_query:
            raise ValueError(f"No embeddings found with the given {query=} with {similarity_threshold=}")

        files_path = (
            Embedding.objects.filter(project=project)
            .values("file_path")  # the combination of values and annotate, is the Django way of making a group by
            .annotate(distance=Min(CosineDistance("embedding", embedded_query[0])))
            .order_by("distance")
            .values_list("file_path", flat=True)
        )[:max_results]

        logger.debug("Files retrieved (using %s):\n %s", self.embedder.__class__.__name__, "\n".join(files_path))
        return list(files_path)

    def reembed_code(
        self,
        project: Project,
        files_texts: Union[str, List[str], List[Tuple[str, str]]],
        embeddings: Any = None,
    ) -> None:
        Embedding.objects.filter(project=project).delete()

        if not embeddings:
            embeddings = self.embed(prompt=files_texts)

        for file_text, file_text_embedding in zip(files_texts, embeddings.embeddings):
            Embedding.objects.create(
                project=project,
                embedding=file_text_embedding,
                file_path=file_text[0],
                text=file_text[1],
            )
