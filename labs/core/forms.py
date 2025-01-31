import os

from core.models import Project, ModelTypeEnum
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


class ModelFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()

        embedding_name = ModelTypeEnum.EMBEDDING.name
        llm_name = ModelTypeEnum.LLM.name
        counts = {
            embedding_name: 0,
            llm_name: 0,
        }
        errors = []

        for form in self.forms:
            model_type = form.cleaned_data["model_type"]
            if model_type in counts and form.cleaned_data["active"]:
                counts[model_type] += 1

        for type_name, count in counts.items():
            if count != 1:
                errors.append(
                    ValidationError(
                        f"You must have exactly 1 active '{type_name}', found {count}."
                    )
                )

        if errors:
            raise ValidationError(errors)
