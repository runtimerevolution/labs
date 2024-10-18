from abc import ABCMeta

from labs.database.vectorize.chunk_vectorizer import ChunkVectorizer
from labs.database.vectorize.python_vectorizer import PythonVectorizer
from enum import Enum

from labs.decorators import time_and_log_function


class VectorizerType(Enum):
    CHUNK = "chunk"
    PYTHON = "python"


class VectorizeFactory(metaclass=ABCMeta):

    def __init__(self, vectorizer: VectorizerType | str = VectorizerType.CHUNK):
        if vectorizer == VectorizerType.CHUNK:
            self.vectorizer = ChunkVectorizer()

        elif vectorizer == VectorizerType.PYTHON:
            self.vectorizer = PythonVectorizer()

        else:
            raise ValueError(f"Expected {VectorizerType} got {vectorizer}")

    @time_and_log_function
    def vectorize_to_database(self, include_file_extensions, repo_destination):
        return self.vectorizer.vectorize_to_database(include_file_extensions, repo_destination)