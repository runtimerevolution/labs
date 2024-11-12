# Generated by Django 5.1.2 on 2024-11-12 16:53

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Config",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("llm_model", models.TextField(blank=True, null=True)),
                (
                    "label",
                    models.CharField(
                        choices=[
                            ("ACTIVELOOP_TOKEN", "ACTIVELOOP_TOKEN"),
                            ("ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY"),
                            ("ANYSCALE_API_KEY", "ANYSCALE_API_KEY"),
                            ("COHERE_API_KEY", "COHERE_API_KEY"),
                            ("GEMINI_API_KEY", "GEMINI_API_KEY"),
                            ("GROQ_API_KEY", "GROQ_API_KEY"),
                            ("HUGGINGFACE_API_KEY", "HUGGINGFACE_API_KEY"),
                            ("LITELLM_API_KEY", "LITELLM_API_KEY"),
                            ("LITELLM_MASTER_KEY", "LITELLM_MASTER_KEY"),
                            ("MISTRAL_API_KEY", "MISTRAL_API_KEY"),
                            ("OPENAI_API_KEY", "OPENAI_API_KEY"),
                        ],
                        max_length=255,
                        verbose_name="Label",
                    ),
                ),
                ("value", models.TextField(blank=True, null=True)),
                (
                    "type",
                    models.CharField(blank=True, max_length=255, null=True, verbose_name="Type"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["label", "llm_model"],
                        name="core_config_label_46669a_idx",
                    )
                ],
            },
        ),
    ]
