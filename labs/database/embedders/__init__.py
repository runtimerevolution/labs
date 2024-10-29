from abc import ABC, abstractmethod


class Embedder(ABC):
    @abstractmethod
    def create_embeddins(self, prompt, **kwargs): ...
