# Generated by Django 3.2.25 on 2024-11-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wirgarten", "0043_productprice_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productcapacity",
            name="capacity",
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
    ]