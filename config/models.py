from django.db import models
from django.utils import timezone

class Config(models.Model):
    llm_model = models.TextField(blank=True, null=True) 
    config_key = models.TextField(unique=True)
    config_value = models.TextField(blank=True, null=True)
    config_type = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.config_key}: {self.config_value}"

    class Meta:
        indexes = [
            models.Index(fields=['config_key', 'llm_model'])
        ]
