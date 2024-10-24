from django.db import models
from django.utils import timezone

class Config(models.Model):
    llm_model = models.TextField(blank=True, null=True) 
    key = models.TextField(unique=True)
    value = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        indexes = [
            models.Index(fields=['key', 'llm_model'])
        ]
