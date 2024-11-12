import logging
import os
from types import SimpleNamespace

import config.configuration_variables as settings
import openai
import pathspec
from embeddings.base import Embedder
from embeddings.openai import OpenAIEmbedder
from embeddings.vectorizers.base import Vectorizer
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from parsers.python import get_lines_code, parse_python_file

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY


class PythonVectorizer(Vectorizer):
    def prepare_doc_content(self, metadata, code_snippet):
        metadata = SimpleNamespace(**metadata)

        result = (
            f"Source: {metadata.source}\n"
            f"Name: {metadata.name}\n"
            f"Start line: {metadata.start_line}\n"
            f"End line: {metadata.end_line}\n"
        )

        if hasattr(metadata, "parameters"):
            result += f"Parameters: {', '.join(metadata.parameters)}\n"

        if hasattr(metadata, "returns"):
            result += f"Returns: {metadata.returns}\n"

        result += f"\n\n{code_snippet}"
        return result

    def load_docs(self, root_dir, file_extensions=None):
        docs = []

        gitignore_path = os.path.join(root_dir, ".gitignore")
        if os.path.isfile(gitignore_path):
            with open(gitignore_path, "r") as gitignore_file:
                gitignore = gitignore_file.read()
            spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore.splitlines())

        else:
            spec = None

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                if file.startswith(".") or file.endswith(".lock"):
                    continue

                if spec and spec.match_file(file_path):
                    continue

                if file_extensions and os.path.splitext(file_path)[1] not in file_extensions:
                    continue

                # only python files
                if os.path.splitext(file_path)[1] != ".py":
                    try:
                        loader = TextLoader(file_path, encoding="utf-8")
                        docs.extend(loader.load_and_split())

                    except Exception:
                        logger.exception("Failed to load repo documents into memory.")

                    continue

                python_file_structure = parse_python_file(file_path)

                # functions
                for func in python_file_structure.get("functions", []):
                    func_ns = SimpleNamespace(**func)

                    function_snippet = get_lines_code(file_path, func_ns.start_line, func_ns.end_line)
                    metadata = dict(
                        source=file_path,
                        name=func_ns.name,
                        start_line=func_ns.start_line,
                        end_line=func_ns.end_line,
                        parameters=func_ns.parameters,
                        returns=func_ns.returns,
                    )

                    doc_content = self.prepare_doc_content(metadata, function_snippet)
                    docs.append(Document(doc_content, metadata=metadata))

                # classes
                for cls in python_file_structure.get("classes", []):
                    cls_ns = SimpleNamespace(**cls)

                    class_snippet = get_lines_code(file_path, cls_ns.start_line, cls_ns.end_line)
                    metadata = dict(
                        source=file_path,
                        name=cls_ns.name,
                        start_line=cls_ns.start_line,
                        end_line=cls_ns.end_line,
                    )

                    doc_content = self.prepare_doc_content(metadata, class_snippet)
                    docs.append(Document(doc_content, metadata=metadata))

                    for method in cls.get("methods"):
                        method_ns = SimpleNamespace(**method)

                        method_snippet = get_lines_code(file_path, method_ns.start_line, method_ns.end_line)
                        metadata = dict(
                            source=file_path,
                            name=method_ns.name,
                            start_line=method_ns.start_line,
                            end_line=method_ns.end_line,
                            parameters=method_ns.parameters,
                            returns=method_ns.returns,
                        )

                        doc_content = self.prepare_doc_content(metadata, method_snippet)
                        docs.append(Document(doc_content, metadata=metadata))

        return docs

    def vectorize_to_database(self, include_file_extensions, repo_destination):
        docs = self.load_docs(repo_destination, include_file_extensions)

        logger.debug(f"Loading {len(docs)} documents...")

        embedder = Embedder(OpenAIEmbedder)
        for doc in docs:
            embeddings = embedder.embed(doc)

            logger.debug("Storing embeddins...")
            embedder.reembed_code(
                files_texts=[(doc.metadata["source"], doc.page_content)],
                embeddings=embeddings,
                repo_destination=repo_destination,
            )
