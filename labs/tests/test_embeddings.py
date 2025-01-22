from core.models import Project
from django.test import TestCase
from embeddings.embedder import Embedder, Embeddings
from embeddings.models import Embedding
from embeddings.openai import OpenAIEmbedder
from tests.constants import OPENAI_LLM_MODEL_NAME
from tests.utilities import create_test_config, generate_random_int_list


class TestEmbeddings(TestCase):
    EMBEDDINGS = [
        {
            "file_path": "file",
            "text": "text",
            "embedding": generate_random_int_list(),
        },
        {
            "file_path": "file1",
            "text": "text1",
            "embedding": generate_random_int_list(),
        },
        {
            "file_path": "file2",
            "text": "text2",
            "embedding": generate_random_int_list(),
        },
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_config()

        cls.project = Project.objects.create(name="test", path="/test/path")

        for embedding in cls.EMBEDDINGS:
            Embedding.objects.create(**embedding, project=cls.project)

    def test_find_embeddings_no_match(self):
        result = Embedding.objects.filter(project=1000).all()
        self.assertEqual(list(result), [])

    def test_find_embeddings_single_match(self):
        new_project = Project(name="test1", path="/test1/path")
        new_project.save()

        Embedding(**self.EMBEDDINGS[0], project=new_project).save()

        result = Embedding.objects.filter(project=new_project)
        self.assertEqual(len(result), 1)

        result = result[0]
        self.assertEqual(result.file_path, self.EMBEDDINGS[0]["file_path"])
        self.assertEqual(result.text, self.EMBEDDINGS[0]["text"])
        self.assertEqual(result.embedding.size, len(self.EMBEDDINGS[0]["embedding"]))

    def test_find_embeddings_multiple_match(self):
        result = Embedding.objects.filter(project=self.project).all()
        for i in range(len(result)):
            embedding: Embedding = result[i]
            self.assertEqual(embedding.file_path, self.EMBEDDINGS[i]["file_path"])
            self.assertEqual(embedding.text, self.EMBEDDINGS[i]["text"])
            self.assertEqual(embedding.embedding.size, len(self.EMBEDDINGS[i]["embedding"]))

    def test_reembed_code(self):
        files_texts = [("file1", "text1"), ("file2", "text2")]
        embeddings = Embeddings(
            model="model",
            embeddings=[
                generate_random_int_list(),
                generate_random_int_list(),
            ],
        )

        Embedder(OpenAIEmbedder, model=OPENAI_LLM_MODEL_NAME).reembed_code(
            project=self.project, files_texts=files_texts, embeddings=embeddings
        )

        result = Embedding.objects.filter(project=self.project).all()
        self.assertEqual(len(result), 2)

        expected_results = self.EMBEDDINGS[1:]
        for i in range(len(result)):
            embedding: Embedding = result[i]
            self.assertEqual(embedding.file_path, expected_results[i]["file_path"])
            self.assertEqual(embedding.text, expected_results[i]["text"])
            self.assertEqual(embedding.embedding.size, len(expected_results[i]["embedding"]))
