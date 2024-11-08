from django.contrib import admin

from .models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("llm_model", "label", "value", "type", "created_at", "updated_at")
    search_fields = ["label", "llm_model"]
