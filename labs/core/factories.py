import factory
from factory.django import DjangoModelFactory

from .models import (
    Model,
    ModelTypeEnum,
    Project,
    Prompt,
    ProviderEnum,
    Variable,
    VectorizerEnum,
    VectorizerModel,
    WorkflowResult,
)

VARIABLES_NAMES = ["OPENAI_API_KEY", "DEFAULT_VECTORIZER", "DEFAULT_PERSONA", "DEFAULT_INSTRUCTION"]
PROVIDERS_VARIABLES = {
    ProviderEnum.NO_PROVIDER.name: ["DEFAULT_VECTORIZER", "DEFAULT_PERSONA", "DEFAULT_INSTRUCTION"],
    ProviderEnum.OPENAI.name: ["OPENAI_API_KEY"],
}
MODELS_TYPES_PROVIDERS = {
    ModelTypeEnum.EMBEDDING.name: [ProviderEnum.OPENAI.name, ProviderEnum.OLLAMA.name],
    ModelTypeEnum.LLM.name: [ProviderEnum.OPENAI.name, ProviderEnum.OLLAMA.name],
}
MODEL_TYPES = [ModelTypeEnum.EMBEDDING.name, ModelTypeEnum.EMBEDDING.name]
PROVIDERS = [ProviderEnum.NO_PROVIDER.name, ProviderEnum.OPENAI.name, ProviderEnum.OLLAMA.name]
VECTORIZERS = [VectorizerEnum.CHUNK_VECTORIZER.name, VectorizerEnum.PYTHON_VECTORIZER.name]


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


class ModelFactory(DjangoModelFactory):
    class Meta:
        model = Model

    model_type = factory.Iterator([mt.name for mt in ModelTypeEnum])
    provider = factory.Iterator([provider.name for provider in ProviderEnum if provider != ProviderEnum.NO_PROVIDER])
    model_name = factory.Faker("word")
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
    project = factory.SubFactory(ProjectFactory)
    task_id = factory.Faker("uuid")
    embed_model = factory.Faker("word")
    prompt_model = factory.Faker("word")
    embeddings = factory.Faker("text")
    context = factory.Faker("text")
    llm_response = factory.Faker("text")
    modified_files = factory.Faker("text")

    class Meta:
        model = WorkflowResult


class PromptFactory(DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    persona = factory.Faker("text")
    instruction = factory.Faker("text")

    class Meta:
        model = Prompt
