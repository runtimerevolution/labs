import os

from core.models import Project
from django import forms
from django.conf import settings


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_projects_directories()

    def get_projects_directories(self):
        directories = []
        for directory in os.listdir(settings.REPOSITORIES_PATH):
            full_directory_path = os.path.join(settings.REPOSITORIES_PATH, directory)
            if os.path.isdir(full_directory_path):
                directories.append((full_directory_path, directory))

        self.fields["path"] = forms.ChoiceField(
            choices=directories,
            label="Project directory",
            required=True,
        )

    class Meta:
        model = Project
        fields = ["name", "description", "path", "url"]
