class Vectorizer:
    def __init__(self, vectorizer, *args, **kwargs):
        self.vectorizer = vectorizer(*args, **kwargs)

    def vectorize_to_database(self, include_file_extensions, repository_path, *args, **kwargs) -> None:
        self.vectorizer.vectorize_to_database(include_file_extensions, repository_path, *args, **kwargs)
