from abc import ABC, abstractmethod


class Vectorizer(ABC):

    @abstractmethod
    def vectorize_to_database(self, include_file_extensions, repo_destination):
        ...