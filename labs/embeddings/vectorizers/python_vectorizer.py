import logging
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Union

import pathspec
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from parsers.python import get_lines_code, parse_python_file

logger = logging.getLogger(__name__)


class PythonVectorizer:
    def __init__(self, embedder):
        self.embedder = embedder

    def load_file_chunks(self, file_path: Union[str, Path]):
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            return loader.load_and_split()

        except Exception:
            logger.exception(f"Error loading file {file_path}")

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

                if os.path.splitext(file_path)[1] != ".py":
                    docs.extend(self.load_file_chunks(file_path))
                    continue

                # Python files with syntax errors will be loaded in chunks
                try:
                    python_file_structure = parse_python_file(file_path)

                except SyntaxError as e:
                    logger.error(f"Syntax error at {file_path}. File will be loaded without Python parsing: {e}")
                    docs.extend(self.load_file_chunks(file_path))
                    continue

                # Functions
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

                    docs.append(Document(function_snippet, metadata=metadata))

                # Classes
                for cls in python_file_structure.get("classes", []):
                    cls_ns = SimpleNamespace(**cls)

                    class_snippet = get_lines_code(file_path, cls_ns.start_line, cls_ns.end_line)
                    metadata = dict(
                        source=file_path,
                        name=cls_ns.name,
                        start_line=cls_ns.start_line,
                        end_line=cls_ns.end_line,
                    )

                    docs.append(Document(class_snippet, metadata=metadata))

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

                        docs.append(Document(method_snippet, metadata=metadata))

        return docs

    def vectorize_to_database(self, include_file_extensions, project, *args, **kwargs):
        docs = self.load_docs(project.path, include_file_extensions)

        logger.debug(f"Loading {len(docs)} documents...")
        texts = []
        files_texts = []
        for doc in docs:
            # Add the file path to the content to allow retrieving the file by its path
            # if it is mentioned in the prompt.
            file_path = doc.metadata["source"]
            content = f"{file_path}\n\n{doc.page_content}"

            files_texts.append((file_path, content))
            texts.append(content)

        embeddings = self.embedder.embed(prompt=texts)

        logger.debug("Storing embeddings...")
        self.embedder.reembed_code(
            project=project,
            files_texts=files_texts,
            embeddings=embeddings,
        )
