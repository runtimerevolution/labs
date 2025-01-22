import random

from core.models import ProviderEnum, Variable


def create_test_config() -> None:
    Variable.objects.create(provider=ProviderEnum.OPENAI.name, name="OPENAI_API_KEY", value="key")
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_VECTORIZER", value="CHUNK_VECTORIZER")
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_PERSONA", value="persona")
    Variable.objects.create(provider=ProviderEnum.NO_PROVIDER.name, name="DEFAULT_INSTRUCTION", value="instruction")


def generate_random_int_list(start: int = 1, end: int = 5000, k: int = 1536) -> list[int]:
    return random.sample(range(start, end), k)
