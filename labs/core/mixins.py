import json

from django.utils.safestring import mark_safe


class DeletePermissionMixin:
    def has_delete_permission(self, request, obj=None):
        resolver_match = request.resolver_match
        if resolver_match:
            app_name = resolver_match.app_name
            view_name = resolver_match.view_name

            return app_name == "admin" and view_name in ["admin:core_project_changelist", "admin:core_project_delete"]
        return False


class JSONFormatterMixin:
    def format_json_field(self, json_data):
        if json_data is None:
            return "-"

        formatted_json = json.dumps(json.loads(json_data), indent=2).replace("\\n", "<br>")
        return mark_safe(f'<pre style="white-space: pre-wrap;">{formatted_json}</pre>')
