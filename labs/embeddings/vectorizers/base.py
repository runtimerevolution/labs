import os
from abc import ABC, abstractmethod

from core.models import Config


class Vectorizer(ABC):
    @abstractmethod
    def vectorize_to_database(self, include_file_extensions, repo_destination): ...
