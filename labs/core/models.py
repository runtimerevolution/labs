import os
from enum import Enum
from typing import Literal, Tuple

from django.db import models
from embeddings.embedder import Embedder
from embeddings.ollama import OllamaEmbedder
from embeddings.openai import OpenAIEmbedder
from embeddings.vectorizers.chunk_vectorizer import ChunkVectorizer
from embeddings.vectorizers.python_vectorizer import PythonVectorizer
from embeddings.vectorizers.vectorizer import Vectorizer
from llm.ollama import OllamaRequester
from llm.openai import OpenAIRequester
from llm.requester import Requester

provider_model_class = {
    "OPENAI": {"embedding": OpenAIEmbedder, "llm": OpenAIRequester},
    "OLLAMA": {"embedding": OllamaEmbedder, "llm": OllamaRequester},
}

vectorizer_model_class = {"CHUNK_VECTORIZER": ChunkVectorizer, "PYTHON_VECTORIZER": PythonVectorizer}


class ModelTypeEnum(Enum):
    EMBEDDING = "Embedding"
    LLM = "LLM"

    @classmethod
    def choices(cls):
        return [(prop.name, prop.value) for prop in cls]


class ProviderEnum(Enum):
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"

    @classmethod
    def choices(cls):
        return [(prop.name, prop.value) for prop in cls]


class VectorizerEnum(Enum):
    CHUNK_VECTORIZER = "File chunks"
    PYTHON_VECTORIZER = "Python structured"

    @classmethod
    def choices(cls):
        return [(prop.name, prop.value) for prop in cls]


class Variable(models.Model):
    provider = models.CharField(choices=ProviderEnum.choices())
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


class Model(models.Model):
    model_type = models.CharField(choices=ModelTypeEnum.choices())
    provider = models.CharField(choices=ProviderEnum.choices())
    model_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_active_embedding_model() -> Tuple[Embedder, str]:
        return Model._get_active_provider_model("embedding")

    @staticmethod
    def get_active_llm_model() -> Tuple[Requester, str]:
        return Model._get_active_provider_model("llm")

    @staticmethod
    def _get_active_provider_model(model_type: Literal["embedding", "llm", "vectorizer"]):
        queryset = Model.objects.filter(model_type=model_type.upper(), active=True)
        if not queryset.exists():
            raise ValueError(f"No {model_type} model configured")

        model = queryset.first()

        # Load associated provider variables
        Variable.load_provider_keys(model.provider)

        return provider_model_class[model.provider][model_type], model.model_name

    def save(self, *args, **kwargs):
        Model.objects.filter(model_type=self.model_type, active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.model_type} {self.provider} {self.model_name}"

    class Meta:
        indexes = [models.Index(fields=["provider", "model_name"])]


class VectorizerModel(models.Model):
    vectorizer_type = models.CharField(choices=VectorizerEnum.choices())
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_active_vectorizer() -> Vectorizer:
        queryset = VectorizerModel.objects.filter(active=True)
        if not queryset.exists():
            raise ValueError("No vectorizer configured")

        vectorizer_model = queryset.first()
        return vectorizer_model_class[vectorizer_model.vectorizer_type]

    def save(self, *args, **kwargs):
        VectorizerModel.objects.filter(active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Vectorizer"
        verbose_name_plural = "Vectorizers"


class WorkflowResult(models.Model):
    task_id = models.CharField(max_length=255)
    embed_model = models.CharField(max_length=255, null=True)
    prompt_model = models.CharField(max_length=255, null=True)
    embeddings = models.TextField(null=True)
    context = models.TextField(null=True)
    llm_response = models.TextField(null=True)
    modified_files = models.TextField(null=True)
    pre_commit_error = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
