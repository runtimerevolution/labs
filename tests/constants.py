import random


def embedding_values() -> list[int]:
    return random.sample(range(1, 5000), 1536)


REPO = "repo"

SINGLE_EMBEDDING = {
    "repository": REPO,
    "file_and_path": "file",
    "text": "text",
    "embedding": embedding_values(),
}

MULTIPLE_EMBEDDINGS = [
    {
        "repository": REPO,
        "file_and_path": "file1",
        "text": "text1",
        "embedding": embedding_values(),
    },
    {
        "repository": REPO,
        "file_and_path": "file2",
        "text": "text2",
        "embedding": embedding_values(),
    },
]
