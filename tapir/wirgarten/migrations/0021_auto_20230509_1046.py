# Generated by Django 3.2.18 on 2023-05-09 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wirgarten", "0020_auto_20230426_1430"),
    ]

    operations = [
        migrations.AddField(
            model_name="questionairetrafficsourceresponse",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]