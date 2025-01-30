import factory
import numpy as np
from core.factories import ProjectFactory

from .models import Embedding


class EmbeddingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Embedding

    project = factory.SubFactory(ProjectFactory)
    file_path = factory.Faker("file_path")
    text = factory.Faker("text")
    embedding = factory.LazyAttribute(lambda _: np.random.rand(300).tolist())
