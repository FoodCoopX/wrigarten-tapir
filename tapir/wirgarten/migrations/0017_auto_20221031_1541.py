# Generated by Django 3.2.16 on 2022-10-31 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wirgarten", "0016_taxrate"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="edited",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[("PAID", "Bezahlt"), ("DUE", "Offen")],
                default="DUE",
                max_length=8,
            ),
        ),
    ]