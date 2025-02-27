# Generated by Django 5.1.5 on 2025-02-27 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_model_provider_alter_variable_provider"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmbeddingModel",
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
                (
                    "provider",
                    models.CharField(
                        choices=[
                            ("NO_PROVIDER", "No provider"),
                            ("OPENAI", "OpenAI"),
                            ("OLLAMA", "Ollama"),
                            ("GEMINI", "Gemini"),
                            ("ANTHROPIC", "Anthropic"),
                        ]
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Ensure this Embedding exists and is downloaded.",
                        max_length=255,
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=True, help_text="Only one Embedding can be active."
                    ),
                ),
            ],
            options={
                "verbose_name": "Embedding",
                "verbose_name_plural": "Embeddings",
            },
        ),
        migrations.CreateModel(
            name="LLMModel",
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
                (
                    "provider",
                    models.CharField(
                        choices=[
                            ("NO_PROVIDER", "No provider"),
                            ("OPENAI", "OpenAI"),
                            ("OLLAMA", "Ollama"),
                            ("GEMINI", "Gemini"),
                            ("ANTHROPIC", "Anthropic"),
                        ]
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Ensure this LLM exists and is downloaded.",
                        max_length=255,
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=True, help_text="Only one LLM can be active."
                    ),
                ),
                (
                    "max_output_tokens",
                    models.IntegerField(
                        blank=True,
                        default=None,
                        help_text="Leave blank for auto-detection, set only if required.",
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "LLM",
                "verbose_name_plural": "LLMs",
            },
        ),
        migrations.DeleteModel(
            name="Model",
        ),
        migrations.AlterField(
            model_name="variable",
            name="value",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="variable",
            unique_together={("provider", "name")},
        ),
        migrations.AddIndex(
            model_name="embeddingmodel",
            index=models.Index(
                fields=["provider", "name"], name="core_embedd_provide_04143f_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="embeddingmodel",
            constraint=models.UniqueConstraint(
                condition=models.Q(("active", True)),
                fields=("provider",),
                name="unique_active_embedding",
            ),
        ),
        migrations.AddIndex(
            model_name="llmmodel",
            index=models.Index(
                fields=["provider", "name"], name="core_llmmod_provide_8330c3_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="llmmodel",
            constraint=models.UniqueConstraint(
                condition=models.Q(("active", True)),
                fields=("provider",),
                name="unique_active_llm",
            ),
        ),
    ]
