# Generated by Django 3.1.8 on 2021-05-31 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coop", "0009_auto_20210529_1248"),
    ]

    operations = [
        migrations.AddField(
            model_name="draftuser",
            name="ratenzahlung",
            field=models.BooleanField(default=False, verbose_name="Ratenzahlung"),
        ),
        migrations.AddField(
            model_name="shareowner",
            name="ratenzahlung",
            field=models.BooleanField(default=False, verbose_name="Ratenzahlung"),
        ),
    ]
