from django.contrib import admin

from .models import Config, Variable


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
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
