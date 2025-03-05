import os

from core.models import Project
from django.forms import (
    ModelForm, BaseModelFormSet, ValidationError, ChoiceField
)
from django.conf import settings


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_projects_directories()

    def get_projects_directories(self):
        directories = []
        for directory in os.listdir(settings.REPOSITORIES_PATH):
            full_directory_path = os.path.join(settings.REPOSITORIES_PATH, directory)
            if os.path.isdir(full_directory_path):
                directories.append((full_directory_path, directory))

        self.fields["path"] = ChoiceField(
            choices=directories,
            label="Project directory",
            required=True,
        )

    class Meta:
        model = Project
        fields = ["name", "description", "path", "url"]


class SingleActiveFormSet(BaseModelFormSet):
    model_name = "Model"

    def clean(self):
        super().clean()
        active_count = sum(
            1 for form in self.forms
            if form.cleaned_data and form.cleaned_data.get("active", False)
        )
        if active_count != 1:
            raise ValidationError(
                f"You must have exactly 1 active {self.model_name}, found {active_count}."
            )

class EmbeddingModelFormSet(SingleActiveFormSet):
    model_name = "Embedding"

class LLMModelFormSet(SingleActiveFormSet):
    model_name = "LLM"