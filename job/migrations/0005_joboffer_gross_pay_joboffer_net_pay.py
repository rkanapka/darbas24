# Generated by Django 5.0.1 on 2024-01-31 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0004_jobcategory_cvbankas_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="joboffer",
            name="gross_pay",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="joboffer",
            name="net_pay",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
