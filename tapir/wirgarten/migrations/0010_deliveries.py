# Generated by Django 3.2.16 on 2022-10-21 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wirgarten", "0009_payment_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Deliveries",
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
                ("delivery_date", models.DateField()),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="wirgarten.member",
                    ),
                ),
            ],
        ),
    ]
