from embeddings.embedder import Embedder, Embeddings
from litellm import embedding


class OpenAIEmbedder(Embedder):
    def __init__(self, model="text-embedding-ada-002"):
        self._model = model

    def embed(self, prompt, *args, **kwargs) -> Embeddings:
        result = embedding(model=self._model, input=prompt, *args, **kwargs)
        return Embeddings(
            model=result.model,
            model_config=result.model_config,
            embeddings=[data["embedding"] for data in result.data],
        )
