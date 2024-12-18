from django.contrib import admin

from .models import Model, Variable, VectorizerModel


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
