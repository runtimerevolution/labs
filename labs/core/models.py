import os
from enum import Enum
from typing import Literal, Tuple

from django.core.exceptions import ValidationError
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
    NO_PROVIDER = "No provider"
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

    def __str__(self):
        return self.name


class Model(models.Model):
    model_type = models.CharField(choices=ModelTypeEnum.choices())
    provider = models.CharField(choices=ProviderEnum.choices())
    model_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class VectorizerModel(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vectorizer_type = models.CharField(choices=VectorizerEnum.choices(), default=Variable.get_default_vectorizer_value)

    @staticmethod
    def get_active_vectorizer(project_id) -> Vectorizer:
        queryset = VectorizerModel.objects.filter(project__id=project_id)
        if not queryset.exists():
            raise ValueError("No vectorizer configured")

        vectorizer_model = queryset.first()
        return vectorizer_model_class[vectorizer_model.vectorizer_type]

    def __str__(self):
        return self.vectorizer_type

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

    def __str__(self):
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

    def __str__(self):
        return f"{self.persona[:50]}..., {self.instruction[:50]}..."

    class Meta:
        verbose_name = "Prompt"
        verbose_name_plural = "Prompts"
