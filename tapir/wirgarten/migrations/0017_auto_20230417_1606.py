# Generated by Django 3.2.18 on 2023-04-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wirgarten", "0016_auto_20230414_1305"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="productcapacity",
            name="idx_productcapacity_period",
        ),
        migrations.AddField(
            model_name="subscription",
            name="solidarity_price_absolute",
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name="producttype",
            name="delivery_cycle",
            field=models.CharField(
                choices=[
                    ("no_delivery", "Keine Lieferung/Abholung"),
                    ("weekly", "1x pro Woche"),
                    ("odd_weeks", "2x pro Monat (ungerade KW)"),
                    ("even_weeks", "2x pro Monat (gerade KW)"),
                ],
                default=("no_delivery", "Keine Lieferung/Abholung"),
                max_length=16,
                verbose_name="Lieferzyklus",
            ),
        ),
    ]
