from django.db import models
from pgvector.django import VectorField


class Embedding(models.Model):
    project = models.ForeignKey("core.Project", on_delete=models.CASCADE)
    repository = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    text = models.TextField()
    embedding = VectorField()

    def __str__(self):
        return self.file_path
