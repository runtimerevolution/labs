import random


def embedding_values() -> list[int]:
    return random.sample(range(1, 5000), 1536)


OPENAI_LLM_MODEL_NAME = "gpt-4o"
OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
OLLAMA_LLM_MODEL_NAME = "llama3.2:latest"
OLLAMA_EMBEDDING_MODEL_NAME = "nomic-embed-text:latest"

SINGLE_EMBEDDING = {
    "file_path": "file",
    "text": "text",
    "embedding": embedding_values(),
}

MULTIPLE_EMBEDDINGS = [
    {
        "file_path": "file1",
        "text": "text1",
        "embedding": embedding_values(),
    },
    {
        "file_path": "file2",
        "text": "text2",
        "embedding": embedding_values(),
    },
]
