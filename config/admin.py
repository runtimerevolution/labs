from django.contrib import admin
from .models import Config

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('llm_model', 'config_key', 'config_value', 'config_type', 'created_at', 'updated_at')
    search_fields = (['config_key', 'llm_model'])
