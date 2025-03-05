import factory
from factory.django import DjangoModelFactory

from .models import (
    LLMModel,
    EmbeddingModel,
    Project,
    Prompt,
    ProviderEnum,
    Variable,
    VectorizerEnum,
    VectorizerModel,
    WorkflowResult,
)

VARIABLES_NAMES = ["OPENAI_API_KEY", "DEFAULT_VECTORIZER", "DEFAULT_PERSONA", "DEFAULT_INSTRUCTION"]


class VariableFactory(DjangoModelFactory):
    class Meta:
        model = Variable

    provider = factory.Iterator([provider.name for provider in ProviderEnum if provider != ProviderEnum.NO_PROVIDER])
    name = factory.Iterator(VARIABLES_NAMES)
    value = factory.Faker("text")

    @factory.post_generation
    def default_vectorizer_value_validation(self, create, extracted, **kwargs):
        if self.name == "DEFAULT_VECTORIZER" and self.value not in ["CHUNK_VECTORIZER", "PYTHON_VECTORIZER"]:
            raise ValueError("Invalid vectorizer value")


class LLMModelFactory(DjangoModelFactory):
    class Meta:
        model = LLMModel

    provider = factory.Iterator([provider.name for provider in ProviderEnum if provider != ProviderEnum.NO_PROVIDER])
    name = factory.Faker("word")
    active = factory.Faker("boolean")
    max_output_tokens = factory.Faker("integer")


class EmbeddingModelFactory(DjangoModelFactory):
    class Meta:
        model = EmbeddingModel

    provider = factory.Iterator([provider.name for provider in ProviderEnum if provider != ProviderEnum.NO_PROVIDER])
    name = factory.Faker("word")
    active = factory.Faker("boolean")


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("word")
    description = factory.Faker("text")
    path = factory.Faker("file_path")
    url = factory.Faker("url")


class VectorizerFactory(DjangoModelFactory):
    class Meta:
        model = VectorizerModel

    project = factory.SubFactory(ProjectFactory)
    vectorizer_type = factory.Iterator([vectorizer.name for vectorizer in VectorizerEnum])

    @factory.post_generation
    def set_vectorizer_type(self, create, extracted, **kwargs):
        if not self.vectorizer_type:
            self.vectorizer_type = "CHUNK_VECTORIZER"


class WorkflowResultFactory(DjangoModelFactory):
    class Meta:
        model = WorkflowResult

    project = factory.SubFactory(ProjectFactory)
    task_id = factory.Faker("uuid")
    embed_model = factory.Faker("word")
    prompt_model = factory.Faker("word")
    embeddings = factory.Faker("text")
    context = factory.Faker("text")
    llm_response = factory.Faker("text")
    modified_files = factory.Faker("text")


class PromptFactory(DjangoModelFactory):
    class Meta:
        model = Prompt

    project = factory.SubFactory(ProjectFactory)
    persona = factory.Faker("text")
    instruction = factory.Faker("text")

    @factory.post_generation
    def set_persona_and_instruction(self, create, extracted, **kwargs):
        if not self.persona:
            self.persona = "Default persona value"
        if not self.instruction:
            self.instruction = "Default instruction value"
