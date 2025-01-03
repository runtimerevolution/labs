import logging

logger = logging.getLogger(__name__)


class Vectorizer:
    def __init__(self, vectorizer, *args, **kwargs):
        self.vectorizer = vectorizer(*args, **kwargs)

    def vectorize_to_database(self, include_file_extensions, repository_path, *args, **kwargs) -> None:
        logger.debug(f"Vectorizing files in {repository_path} (using {self.vectorizer.__class__.__name__})")
        self.vectorizer.vectorize_to_database(include_file_extensions, repository_path, *args, **kwargs)
