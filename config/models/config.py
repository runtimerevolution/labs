from django.db import models
from django.utils import timezone

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
    key = models.TextField(unique=True, choices=[(k, k) for k in sorted(AVAILABLE_KEYS)])
    value = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        indexes = [models.Index(fields=["llm_model", "key"])]
