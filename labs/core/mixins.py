import json

from django.utils.safestring import mark_safe


class JSONFormatterMixin:
    def format_json_field(self, json_data):
        if json_data is None:
            return "-"

        formatted_json = json.dumps(json.loads(json_data), indent=2).replace("\\n", "<br>")
        return mark_safe(f'<pre style="white-space: pre-wrap;">{formatted_json}</pre>')
