from django.contrib import admin
from django.urls import reverse

from .forms import ProjectForm, EmbeddingModelFormSet, LLMModelFormSet
from .mixins import JSONFormatterMixin
from .models import (
    EmbeddingModel, LLMModel, Project, Prompt, 
    Variable, VectorizerModel, WorkflowResult
)

@admin.register(EmbeddingModel)
class EmbeddingModelAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "name", "active")
    list_display_links = ("id",)
    list_editable = ("name", "active")
    list_filter = ("provider", "name")
    search_fields = ("provider", "name")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_changelist_formset(self, request, **kwargs):
        kwargs["formset"] = EmbeddingModelFormSet
        return super().get_changelist_formset(request, **kwargs)


@admin.register(LLMModel)
class LLMModelAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "name", "max_output_tokens", "active")
    list_display_links = ("id",)
    list_editable = ("name", "max_output_tokens", "active")
    list_filter = ("provider", "name")
    search_fields = ("provider", "name", "max_output_tokens")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_changelist_formset(self, request, **kwargs):
        kwargs["formset"] = LLMModelFormSet
        return super().get_changelist_formset(request, **kwargs)


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
class VectorizerModelAdmin(admin.ModelAdmin):
    actions = None
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

    def has_delete_permission(self, request, obj=None):
        # The ´Vectorizer´ should only be deleted through the Project (CASCADE)
        # User can type the delete url in the browser, what should not be allowed
        if obj and request.path == reverse("admin:core_vectorizermodel_delete", args=[obj.id]):
            return False
        return bool(obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Remove the admin delete button because ´Vectorizer´ should only be deleted through the Project (CASCADE)
        extra_context = extra_context or {}
        extra_context["show_delete"] = False
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    actions = None
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

    def has_delete_permission(self, request, obj=None):
        # The ´Prompt´ should only be deleted through the Project (CASCADE)
        # User can type the delete url in the browser, what should not be allowed
        if obj and request.path == reverse("admin:core_prompt_delete", args=[obj.id]):
            return False
        return bool(obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Remove the admin delete button because ´Prompt´ should only be deleted through the Project (CASCADE)
        extra_context = extra_context or {}
        extra_context["show_delete"] = False
        return super().change_view(request, object_id, form_url, extra_context)

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
class WorkflowResultAdmin(admin.ModelAdmin, JSONFormatterMixin):
    actions = None
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

    def has_delete_permission(self, request, obj=None):
        # The ´WorkflowResult´ should only be deleted through the Project (CASCADE)
        # User can type the delete url in the browser, what should not be allowed
        if obj and request.path == reverse("admin:core_workflowresult_delete", args=[obj.id]):
            return False
        return bool(obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Remove the admin delete button because ´WorkflowResult´ should only be deleted through the Project (CASCADE)
        extra_context = extra_context or {}
        extra_context["show_delete"] = False
        return super().change_view(request, object_id, form_url, extra_context)

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
