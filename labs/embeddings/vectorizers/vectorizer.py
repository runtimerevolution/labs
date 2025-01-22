import logging

logger = logging.getLogger(__name__)


class Vectorizer:
    def __init__(self, vectorizer, *args, **kwargs):
        self.vectorizer = vectorizer(*args, **kwargs)

    def vectorize_to_database(self, include_file_extensions, project, *args, **kwargs) -> None:
        logger.debug(f"Vectorizing files in {project.path} (using {self.vectorizer.__class__.__name__})")
        self.vectorizer.vectorize_to_database(include_file_extensions, project, *args, **kwargs)
