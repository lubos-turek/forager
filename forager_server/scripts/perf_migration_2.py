# Generated by Django 3.1.1 on 2021-06-03 06:21

from django.db import migrations, models


APP_NAME = "forager_server_api"


class Migration(migrations.Migration):
    dependencies = [
        ("forager_server_api", "perf_migration_1"),
    ]

    operations = [
        migrations.RemoveField("DatasetItem", "google"),
        migrations.RemoveField("Annotation", "label_function"),
        migrations.RemoveField("Annotation", "label_category"),
        migrations.RemoveField("Annotation", "label_type"),
        migrations.RemoveField("Annotation", "label_data"),
        migrations.RemoveField("Annotation", "last_updated"),
        migrations.AlterField(
            "Annotation",
            "user",
            models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to=f"{APP_NAME}.user",
            ),
        ),
        migrations.AlterField(
            "Annotation",
            "category",
            models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to=f"{APP_NAME}.category",
            ),
        ),
        migrations.AlterField(
            "Annotation",
            "mode",
            models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to=f"{APP_NAME}.mode",
            ),
        ),
    ]
