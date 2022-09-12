# Generated by Django 3.2.12 on 2022-09-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Parameter",
            fields=[
                (
                    "key",
                    models.CharField(
                        editable=False,
                        max_length=256,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("description", models.CharField(max_length=512)),
                ("category", models.CharField(max_length=256)),
                ("datatype", models.CharField(editable=False, max_length=8)),
                ("value", models.CharField(max_length=4096, null=True)),
            ],
        ),
    ]