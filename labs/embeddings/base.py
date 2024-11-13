from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

from core.models import Embedding
from sqlalchemy import Connection, Row, delete, insert, select


@dataclass
class Embeddings:
    model: str
    embeddings: List[Dict[str, Any]]
    model_config: Optional[Dict[str, Any]] = None


class Embedder(ABC):
    def __init__(self, embedder: type["Embedder"], *args, **kwargs):
        if not issubclass(embedder, Embedder):
            raise TypeError(f"embedder must be a subclass {Embedder}")
        self.embedder = embedder(*args, **kwargs)

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        return self.embedder.embed(prompt, *args, **kwargs)

    def retrieve_embeddings(
        self, query: str, similarity_threshold: int = 0.7, number_of_results: int = 10
    ) -> Sequence[Row]:
        query = query.replace("\n", "")
        embedded_query = self.embed(prompt=query).embeddings[0]

        cosine_distance = Embedding.embedding.cosine_distance(embedded_query).label("distance")
        return Embedding.objects.filter(cosine_distance < cosine_distance).order_by("distance").limit(number_of_results)
        # TODO: query
        # db_query = (
        #     select(EmbeddingModel, cosine_distance)
        #     .where(cosine_distance < similarity_threshold)
        #     .order_by("distance")
        #     .limit(number_of_results)
        # )
        # return connection.execute(db_query).fetchall()

    def reembed_code(
        self,
        repository: str,
        files_texts: Union[str, List[str]],
        embeddings: Any = None,
    ) -> None:
        Embedding.objects.filter(repository=repository).delete()
        # TODO: query
        # db_query = delete(EmbeddingModel).where(EmbeddingModel.repository == repository)
        # connection.execute(db_query)

        if not embeddings:
            embeddings = self.embed(prompt=files_texts)

        for file_text, file_text_embedding in zip(files_texts, embeddings.embeddings):
            Embedding.objects.create(
                repository=repository,
                embedding=file_text_embedding,
                file_path=file_text[0],
                text=file_text[1],
            )

            # TODO: query
        #     query = insert(EmbeddingModel).values(
        #         repository=repository,
        #         embedding=file_text_embedding,
        #         file_path=file_text[0],
        #         text=file_text[1],
        #     )
        #     connection.execute(query)
        # connection.commit()
