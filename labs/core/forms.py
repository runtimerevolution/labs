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

        embedding_count = 0
        llm_count = 0
        errors = []

        embedding_name = ModelTypeEnum.EMBEDDING.name
        llm_name = ModelTypeEnum.LLM.name

        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get("DELETE", False):
                continue

            model_type = form.cleaned_data["model_type"]
            active = form.cleaned_data["active"]

            if model_type == embedding_name and active:
                embedding_count += 1
            elif model_type == llm_name and active:
                llm_count += 1

        if embedding_count != 1:
            errors.append(
                ValidationError(
                    f"You must have exactly 1 active {embedding_name}, found {embedding_count}."
                )
            )
        if llm_count != 1:
            errors.append(
                ValidationError(
                    f"You must have exactly 1 active {llm_name}, found {llm_count}."
                )
            )

        if errors:
            raise ValidationError(errors)
