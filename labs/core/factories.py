from typing import Dict, Iterable

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

    @classmethod
    def predefined(cls):
        variables_objects = []
        for provider_name in PROVIDERS_VARIABLES:
            for variable_name in PROVIDERS_VARIABLES[provider_name]:
                variables_objects.append(VariableFactory.create(provider=provider_name, name=variable_name))

        return variables_objects


class ModelFactory(DjangoModelFactory):
    model_type = PROVIDERS
    provider = MODEL_TYPES
    model_name = factory.Faker("word")
    active = factory.Faker("boolean")

    @classmethod
    def predefined(cls):
        models_objects = []
        for model_type_name in MODELS_TYPES_PROVIDERS:
            for provider_name in MODELS_TYPES_PROVIDERS[model_type_name]:
                models_objects.append(ModelFactory.create(model_type=model_type_name, provider=provider_name))

        return models_objects

    class Meta:
        model = Model


class ProjectFactory(DjangoModelFactory):
    name = factory.Faker("word")
    description = factory.Faker("text")
    path = factory.Faker("file_path")
    url = factory.Faker("url")

    @classmethod
    def _create(cls, model_class, create_variables: Iterable[Dict[str, str]] = None, *args, **kwargs):
        if create_variables:
            if isinstance(create_variables, Iterable):
                for variable_data in create_variables:
                    VariableFactory.create(**variable_data)
            else:
                raise ValueError("create_variables must be an iterable of dictionaries.")
        else:
            VariableFactory.predefined()

        return super()._create(model_class, *args, **kwargs)

    class Meta:
        model = Project


class VectorizerFactory(DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    vectorizer_type = VECTORIZERS

    class Meta:
        model = VectorizerModel


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
