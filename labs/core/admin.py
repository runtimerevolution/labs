import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Model, Variable, VectorizerModel, WorkflowResult


class JSONFormatterMixin:
    def format_json_field(self, json_data):
        if json_data is None:
            return "-"

        formatted_json = json.dumps(json.loads(json_data), indent=2).replace("\\n", "<br>")
        return mark_safe(f'<pre style="white-space: pre-wrap;">{formatted_json}</pre>')


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "model_type",
        "provider",
        "model_name",
        "active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    list_editable = ("model_type", "provider", "model_name", "active")
    list_filter = ("provider", "model_name")
    search_fields = ("provider", "model_name")


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "provider",
        "name",
        "value",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    list_editable = ("provider", "name", "value")
    list_filter = ("provider", "name")
    search_fields = ("provider", "name")


@admin.register(VectorizerModel)
class VectorizerModel(admin.ModelAdmin):
    list_display = (
        "id",
        "vectorizer_type",
        "active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    list_editable = ("vectorizer_type", "active")
    list_filter = ("vectorizer_type",)
    search_fields = ("vectorizer_type",)


@admin.register(WorkflowResult)
class WorkflowResultAdmin(admin.ModelAdmin, JSONFormatterMixin):
    list_display = ("task_id", "created_at")
    list_display_links = ("task_id",)
    search_fields = ("task_id",)
    readonly_fields = (
        "task_id",
        "created_at",
        "embed_model",
        "prompt_model",
        "pretty_embeddings",
        "pretty_llm_response",
        "pretty_modified_files",
        "pretty_pre_commit_error",
        "pretty_context",
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

    def has_delete_permission(self, request, obj=None):
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
