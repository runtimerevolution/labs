from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

from sqlalchemy import Connection, Row, delete, insert, select

from labs.database.connect import db_connector
from labs.database.models import EmbeddingModel


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

    @db_connector()
    def retrieve_embeddings(
        self, connection: Connection, query: str, similarity_threshold: int = 0.7, number_of_results: int = 10
    ) -> Sequence[Row]:
        query = query.replace("\n", "")
        embedded_query = self.embed(prompt=query).embeddings[0]

        cosine_distance = EmbeddingModel.embedding.cosine_distance(embedded_query).label("distance")
        db_query = (
            select(EmbeddingModel, cosine_distance)
            .where(cosine_distance < similarity_threshold)
            .order_by("distance")
            .limit(number_of_results)
        )
        return connection.execute(db_query).fetchall()

    @db_connector()
    def reembed_code(
        self,
        connection: Connection,
        repository: str,
        files_texts: Union[str, List[str]],
        embeddings: Any = None,
    ) -> None:
        db_query = delete(EmbeddingModel).where(EmbeddingModel.repository == repository)
        connection.execute(db_query)

        if not embeddings:
            embeddings = self.embed(prompt=files_texts)

        for file_text, file_text_embedding in zip(files_texts, embeddings.embeddings):
            query = insert(EmbeddingModel).values(
                repository=repository,
                embedding=file_text_embedding,
                file_path=file_text[0],
                text=file_text[1],
            )
            connection.execute(query)
        connection.commit()
