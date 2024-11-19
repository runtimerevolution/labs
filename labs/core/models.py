import os
from enum import Enum
from typing import Literal, Tuple

from django.db import models
from embeddings.embedder import Embedder
from embeddings.ollama import OllamaEmbedder
from embeddings.openai import OpenAIEmbedder
from litellm_service.ollama import OllamaRequester
from litellm_service.openai import OpenAIRequester

provider_model_class = {
    "OPENAI": {"embedding": OpenAIEmbedder, "llm": OpenAIRequester},
    "OLLAMA": {"embedding": OllamaEmbedder, "llm": OllamaRequester},
}


class Providers(Enum):
    OPENAI = "OPENAI"
    OLLAMA = "OLLAMA"

    @classmethod
    def choices(cls):
        return [(prop.value, prop.name) for prop in cls]


class Variable(models.Model):
    provider = models.CharField(choices=Providers.choices())
    name = models.CharField(max_length=255)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def load_provider_keys(provider: str):
        variables = Variable.objects.filter(provider=provider)
        for variable in variables:
            os.environ.setdefault(variable.name, variable.value)

    def __str__(self):
        return self.name


class Config(models.Model):
    model_type = models.CharField(choices=[("EMBEDDING", "EMBEDDING"), ("LLM", "LLM")])
    provider = models.CharField(choices=Providers.choices())
    model_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_active_embedding_model() -> Tuple[Embedder, str]:
        return Config._get_active_provider_model("embedding")

    @staticmethod
    def get_active_llm_model():
        return Config._get_active_provider_model("llm")

    @staticmethod
    def _get_active_provider_model(model_type: Literal["embedding", "llm"]):
        queryset = Config.objects.filter(model_type=model_type.upper(), active=True)
        if not queryset.exists():
            raise ValueError(f"No {model_type} model configured")

        config = queryset.first()

        # Load associated provider variables
        Variable.load_provider_keys(config.provider)

        return provider_model_class[config.provider][model_type], config.model_name

    def save(self, *args, **kwargs):
        Config.objects.filter(model_type=self.model_type, active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.model_type} {self.provider} {self.model_name}"

    class Meta:
        indexes = [models.Index(fields=["provider", "model_name"])]
