from django.db import models

class LLMSettings(models.Model):
    model_name = models.TextField()  # Identifier for the LLM
    api_key = models.TextField()  # API key for the LLM
    response_format = models.TextField()  # Format of the response (e.g., JSON, text)
    endpoint = models.URLField()  # API endpoint URL for the LLM
    extra_params = models.JSONField(blank=True, null=True)  # Optional field for any extra parameters

    def __str__(self):
        return self.model_name
