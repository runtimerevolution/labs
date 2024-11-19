import logging
import os

import pathspec
from core.models import Config
from embeddings.base import Embedder
from embeddings.vectorizers.base import Vectorizer
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

logger = logging.getLogger(__name__)


class ChunkVectorizer(Vectorizer):
    def load_docs(self, root_dir, file_extensions=None):
        """
        Load documents from the specified root directory.
        Ignore dotfiles, dot directories, and files that match .gitignore rules.
        Optionally filter by file extensions.
        """
        docs = []

        # Load .gitignore rules
        gitignore_path = os.path.join(root_dir, ".gitignore")

        if os.path.isfile(gitignore_path):
            with open(gitignore_path, "r") as gitignore_file:
                gitignore = gitignore_file.read()
            spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore.splitlines())
        else:
            spec = None

        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Remove dot directories from the list of directory names
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

            for file in filenames:
                file_path = os.path.join(dirpath, file)

                if file.startswith("."):
                    continue
                if file.endswith(".lock"):
                    continue

                # Skip files that match .gitignore rules
                if spec and spec.match_file(file_path):
                    continue

                if file_extensions and os.path.splitext(file)[1] not in file_extensions:
                    continue

                try:
                    loader = TextLoader(file_path, encoding="utf-8")
                    docs.extend(loader.load_and_split())
                except Exception:
                    logger.exception("Failed to load repo documents into memory.")
        return docs

    def split_docs(self, docs):
        """Split the input documents into smaller chunks."""
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        return text_splitter.split_documents(docs)

    def vectorize_to_database(self, include_file_extensions, repo_destination):
        logger.debug("Loading and splitting all documents into chunks.")
        docs = self.load_docs(repo_destination, include_file_extensions)
        texts = self.split_docs(docs)
        files_and_texts = [(text.metadata["source"], text.page_content) for text in texts]
        texts = [file_and_text[1] for file_and_text in files_and_texts]

        logger.debug("Embedding all repo documents.")

        embedder_class, *embeder_args = Config.get_active_embedding_model()
        embedder = Embedder(embedder_class, *embeder_args)
        embeddings = embedder.embed(prompt=texts)

        logger.debug("Storing all embeddings.")
        embedder.reembed_code(files_texts=files_and_texts, embeddings=embeddings, repository=repo_destination)  # type: ignore
