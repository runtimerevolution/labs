from core.factories import ProjectFactory
from core.models import Project, Prompt, VectorizerModel
from django.test import TestCase


class FactoryTestCase(TestCase):
    def test_project_models_dependencies(self):
        project_name = "project"
        ProjectFactory.create(name=project_name)

        project = Project.objects.get(name=project_name)
        self.assertEqual(project.name, project_name)

        vectorizer = VectorizerModel.objects.get(project=project)
        self.assertEqual(project.id, vectorizer.project.id)

        prompt = Prompt.objects.get(project=project)
        self.assertEqual(project.id, prompt.id)
