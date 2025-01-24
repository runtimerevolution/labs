from django.contrib import admin

from .forms import ProjectForm
from .mixins import DeletePermissionMixin, JSONFormatterMixin
from .models import Model, Project, Prompt, Variable, VectorizerModel, WorkflowResult


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "model_type",
        "provider",
        "model_name",
        "active",
    )
    list_display_links = ("id",)
    list_editable = ("model_type", "provider", "model_name", "active")
    list_filter = ("provider", "model_name")
    search_fields = ("provider", "model_name")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "provider",
        "name",
        "value",
    )
    list_display_links = ("id",)
    list_editable = ("provider", "value")
    list_filter = ("provider", "name")
    search_fields = ("provider", "name")
    readonly_fields = ("name",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(VectorizerModel)
class VectorizerModelAdmin(admin.ModelAdmin, DeletePermissionMixin):
    list_display = (
        "id",
        "project",
        "vectorizer_type",
    )
    list_display_links = ("id",)
    list_editable = ("vectorizer_type",)
    list_filter = ("vectorizer_type",)
    search_fields = ("vectorizer_type",)

    def has_add_permission(self, request):
        return False


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin, DeletePermissionMixin):
    list_display = (
        "id",
        "project",
        "persona_preview",
        "instruction_preview",
    )
    list_display_links = ("id",)
    search_fields = ("prompt",)

    def has_add_permission(self, request):
        return False

    def persona_preview(self, obj):
        return self.text_preview(obj.persona)

    def instruction_preview(self, obj):
        return self.text_preview(obj.instruction)

    @staticmethod
    def text_preview(text, preview_size=50):
        return f"{text[:preview_size]}..." if len(text) > preview_size else text


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = (
        "id",
        "name",
        "path",
        "url",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("name", "path", "url")
    readonly_fields = ("url",)


@admin.register(WorkflowResult)
class WorkflowResultAdmin(admin.ModelAdmin, DeletePermissionMixin, JSONFormatterMixin):
    list_display = ("task_id", "created_at")
    list_display_links = ("task_id",)
    search_fields = ("task_id",)
    readonly_fields = (
        "project",
        "task_id",
        "created_at",
        "embed_model",
        "prompt_model",
        "pretty_embeddings",
        "pretty_context",
        "pretty_llm_response",
        "pretty_modified_files",
        "pretty_pre_commit_error",
    )
    exclude = (
        "embeddings",
        "context",
        "llm_response",
        "modified_files",
        "pre_commit_error",
    )

    def has_add_permission(self, request):
        return False

    def pretty_embeddings(self, obj):
        return self.format_json_field(obj.embeddings)

    def pretty_context(self, obj):
        return self.format_json_field(obj.context)

    def pretty_llm_response(self, obj):
        return self.format_json_field(obj.llm_response)

    def pretty_modified_files(self, obj):
        return self.format_json_field(obj.modified_files)

    def pretty_pre_commit_error(self, obj):
        return self.format_json_field(obj.pre_commit_error)

    pretty_embeddings.short_description = "Embeddings"
    pretty_context.short_description = "Context"
    pretty_llm_response.short_description = "LLM Response"
    pretty_modified_files.short_description = "Modified Files"
    pretty_pre_commit_error.short_description = "Pre-Commit error message"
