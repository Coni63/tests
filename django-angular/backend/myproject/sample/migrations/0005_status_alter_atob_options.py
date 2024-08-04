# Generated by Django 5.0.7 on 2024-08-04 18:48

from django.db import migrations, models

import pandas as pd

from ..models import Status

def load_csv_data(apps, schema_editor):
    df = pd.read_pickle("../data.pkl")

    for _, row in df.iterrows():
        Status.objects.create(
            message_id =row["message_id"],
            documentum_id =row["documentum_id"],
            publication_id =row["publication_id"],
            status =row["status"],
            status_message =row["status_message"],
            created_at =row["created_at"],
            updated_at =row["updated_at"],
            message =row["message"],
        )

class Migration(migrations.Migration):

    dependencies = [
        ("sample", "0004_atob_sort_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Status",
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
                ("message_id", models.CharField(max_length=10, blank=True)),
                ("documentum_id", models.CharField(max_length=100, blank=True)),
                ("publication_id", models.CharField(max_length=100, blank=True)),
                ("status", models.CharField(max_length=20, blank=True)),
                ("status_message", models.CharField(max_length=100, blank=True)),
                ("created_at", models.DateTimeField(blank=True)),
                ("updated_at", models.DateTimeField(blank=True)),
                ("message", models.JSONField(blank=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name="atob",
            options={"ordering": ["sort_order"]},
        ),
        migrations.RunPython(load_csv_data),
    ]
