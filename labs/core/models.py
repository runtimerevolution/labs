from django.db import models
from pgvector.django import VectorField

AVAILABLE_KEYS = [
    "LITELLM_MASTER_KEY",
    "LITELLM_API_KEY",
    "HUGGINGFACE_API_KEY",
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "COHERE_API_KEY",
    "GROQ_API_KEY",
    "ANTHROPIC_API_KEY",
    "MISTRAL_API_KEY",
    "ANYSCALE_API_KEY",
    "ACTIVELOOP_TOKEN",
]


class Config(models.Model):
    llm_model = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=255, choices=[(k, k) for k in sorted(AVAILABLE_KEYS)], verbose_name="Label")
    value = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

    class Meta:
        indexes = [models.Index(fields=["label", "llm_model"])]


class Embedding(models.Model):
    repository = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    text = models.TextField()
    embedding = VectorField()

    def __str__(self):
        return self.file_path
