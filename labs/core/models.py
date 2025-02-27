import os
from enum import Enum
from typing import Tuple

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from embeddings.embedder import Embedder
from embeddings.gemini import GeminiEmbedder
from embeddings.ollama import OllamaEmbedder
from embeddings.openai import OpenAIEmbedder
from embeddings.vectorizers.chunk_vectorizer import ChunkVectorizer
from embeddings.vectorizers.python_vectorizer import PythonVectorizer
from embeddings.vectorizers.vectorizer import Vectorizer
from llm.anthropic import AnthropicRequester
from llm.gemini import GeminiRequester
from llm.ollama import OllamaRequester
from llm.openai import OpenAIRequester
from llm.requester import Requester

provider_model_class = {
    "OPENAI": {"embedding": OpenAIEmbedder, "llm": OpenAIRequester},
    "OLLAMA": {"embedding": OllamaEmbedder, "llm": OllamaRequester},
    "GEMINI": {"embedding": GeminiEmbedder, "llm": GeminiRequester},
    "ANTHROPIC": {"llm": AnthropicRequester},
}

vectorizer_model_class = {
    "CHUNK_VECTORIZER": ChunkVectorizer, 
    "PYTHON_VECTORIZER": PythonVectorizer,
}

class ProviderEnum(Enum):
    NO_PROVIDER = "No provider"
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"
    GEMINI = "Gemini"
    ANTHROPIC = "Anthropic"

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

    @staticmethod
    def get_default_vectorizer_value():
        return Variable.objects.get(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_VECTORIZER").value

    @staticmethod
    def get_default_persona_value():
        return Variable.objects.get(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_PERSONA").value

    @staticmethod
    def get_default_instruction_value():
        return Variable.objects.get(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_INSTRUCTION").value

    @staticmethod
    def load_provider_keys(provider: str):
        variables = Variable.objects.filter(provider=provider)
        for variable in variables:
            os.environ.setdefault(variable.name, variable.value)

    def clean(self):
        self._default_vectorizer_value_validation()

    def _default_vectorizer_value_validation(self):
        allowed_vectorizer_values = VectorizerEnum.__members__.keys()
        if self.name == "DEFAULT_VECTORIZER" and self.value not in allowed_vectorizer_values:
            raise ValidationError(
                f"The only possible values for DEFAULT_VECTORIZER are: {', '.join(allowed_vectorizer_values)}"
            )

    def __str__(self) -> str:
        return self.name


class EmbeddingModel(models.Model):
    provider = models.CharField(choices=ProviderEnum.choices())
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    @classmethod
    def get_active_model(cls) -> Tuple[Embedder, "EmbeddingModel"]:
        try:
            model = cls.objects.get(active=True)
        except cls.DoesNotExist:
            raise ValueError("No active embedding model configured")

        Variable.load_provider_keys(model.provider)

        try:
            embedder_class = provider_model_class[model.provider]["embedding"]
        except KeyError:
            raise ValueError(f"Provider '{model.provider}' is missing or has no embedder class defined.")

        return embedder_class, model

    def __str__(self) -> str:
        return f"EmbeddingModel [{self.provider}] {self.name}"

    class Meta:
        verbose_name = "Embedding"
        verbose_name_plural = "Embeddings"
        constraints = [
            models.UniqueConstraint(
                fields=["provider"],
                condition=Q(active=True),
                name="unique_active_embedding",
            )
        ]
        indexes = [models.Index(fields=["provider", "name"])]


class LLMModel(models.Model):
    provider = models.CharField(choices=ProviderEnum.choices())
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    max_output_tokens = models.IntegerField(null=True, blank=True, default=None)

    @classmethod
    def get_active_model(cls) -> Tuple[Requester, "LLMModel"]:
        try:
            model = cls.objects.get(active=True)
        except cls.DoesNotExist:
            raise ValueError("No active llm model configured")

        Variable.load_provider_keys(model.provider)

        try:
            llm_class = provider_model_class[model.provider]["llm"]
        except KeyError:
            raise ValueError(f"Provider '{model.provider}' is missing or has no LLM class defined.")

        return llm_class, model

    def __str__(self) -> str:
        return f"LLMModel [{self.provider}] {self.name}"

    class Meta:
        verbose_name = "LLM"
        verbose_name_plural = "LLMs"
        constraints = [
            models.UniqueConstraint(
                fields=["provider"],
                condition=Q(active=True),
                name="unique_active_llm",
            )
        ]
        indexes = [models.Index(fields=["provider", "name"])]


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not os.path.exists(self.path):
            raise ValidationError({"path": f'Directory "{self.path}" does not exist.'})

    def save(self, *args, **kwargs):
        created = not self.id
        super().save(*args, **kwargs)

        if created:
            VectorizerModel.objects.create(project=self)
            Prompt.objects.create(project=self)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class VectorizerModel(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vectorizer_type = models.CharField(choices=VectorizerEnum.choices(), default=Variable.get_default_vectorizer_value)

    @staticmethod
    def get_active_vectorizer(project_id: int) -> Vectorizer:
        vector_model = VectorizerModel.objects.filter(project__id=project_id).first()
        if not vector_model:
            raise ValueError("No vectorizer configured for this project.")
        
        try:
            vec_class = vectorizer_model_class[vector_model.vectorizer_type]
        except KeyError:
            raise ValueError(f"Unrecognized vectorizer type '{vector_model.vectorizer_type}'")

        return vec_class

    def __str__(self) -> str:
        return f"{self.vectorizer_type} for {self.project.name}"

    class Meta:
        verbose_name = "Vectorizer"
        verbose_name_plural = "Vectorizers"


class WorkflowResult(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255)
    embed_model = models.CharField(max_length=255, null=True)
    prompt_model = models.CharField(max_length=255, null=True)
    embeddings = models.TextField(null=True)
    context = models.TextField(null=True)
    llm_response = models.TextField(null=True)
    modified_files = models.TextField(null=True)
    pre_commit_error = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.task_id}"

    class Meta:
        verbose_name = "Workflow result"
        verbose_name_plural = "Workflow results"


class Prompt(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    persona = models.TextField(
        null=False,
        blank=False,
        default=Variable.get_default_persona_value,
        help_text="""It should include additional information to help guide the model's behavior and 
        understanding of its role.""",
    )
    instruction = models.TextField(
        null=False,
        blank=False,
        default=Variable.get_default_instruction_value,
        help_text="""It should include guidelines on what is expected in the generated code, 
        such as "avoid complexity" or "minimize the code".""",
    )

    @staticmethod
    def get_persona(project_id: int) -> str:
        queryset = Prompt.objects.filter(project=project_id)
        if not queryset.exists():
            raise ValueError("No persona configured")

        return queryset.first().persona

    @staticmethod
    def get_instruction(project_id: int) -> str:
        queryset = Prompt.objects.filter(project=project_id)
        if not queryset.exists():
            raise ValueError("No instruction configured")

        return queryset.first().instruction

    def __str__(self) -> str:
        return f"{self.persona[:50]}..., {self.instruction[:50]}..."

    class Meta:
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"
