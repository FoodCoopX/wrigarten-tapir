# Generated by Django 3.2.25 on 2024-10-22 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wirgarten", "0041_auto_20241015_1109"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="is_student",
            field=models.BooleanField(default=False, verbose_name="Student*in"),
        ),
    ]