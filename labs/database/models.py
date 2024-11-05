import logging

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String

from labs.database.connect import Base

logger = logging.getLogger(__name__)


class EmbeddingModel(Base):
    __tablename__ = "embeddings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    repository = Column(String)
    file_path = Column(String)
    text = Column(String)
    embedding = Column(Vector())
