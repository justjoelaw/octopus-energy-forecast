# Generated by Django 4.1.5 on 2023-01-12 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy_tracker', '0006_historical_electric_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictions',
            name='sum_predicted_usage',
            field=models.FloatField(default=666),
            preserve_default=False,
        ),
    ]
