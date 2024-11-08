from django.contrib import admin

from .models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("llm_model", "label", "value", "type", "created_at", "updated_at")
    list_display_links = ("llm_model",)
    list_editable = ("label", "value", "type")
    list_filter = ("llm_model", "label", "value")
    search_fields = ("llm_model", "label")
