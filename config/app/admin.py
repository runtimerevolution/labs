from django.contrib import admin

from .models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("llm_model", "key", "value", "type", "updated_at")
    list_display_links = ("llm_model",)
    list_editable = ("key", "value", "type")
    list_filter = ("llm_model", "key", "value")
    search_fields = ("llm_model", "key", "value")
