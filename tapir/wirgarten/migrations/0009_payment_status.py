# Generated by Django 3.2.16 on 2022-10-21 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wirgarten", "0008_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[
                    ("UPCOMING", "Bevorstehend"),
                    ("PAID", "Bezahlt"),
                    ("DUE", "Offen"),
                ],
                default="DUE",
                max_length=8,
            ),
        ),
    ]