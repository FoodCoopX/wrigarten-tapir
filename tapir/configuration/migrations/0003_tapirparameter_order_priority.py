# Generated by Django 3.2.16 on 2022-10-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configuration", "0002_tapirparameter_label"),
    ]

    operations = [
        migrations.AddField(
            model_name="tapirparameter",
            name="order_priority",
            field=models.IntegerField(default=-1),
        ),
    ]
