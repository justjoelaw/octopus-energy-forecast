# Generated by Django 4.1.5 on 2023-01-10 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energy_tracker', '0002_historical_plots'),
    ]

    operations = [
        migrations.AddField(
            model_name='historical_plots',
            name='plot_type',
            field=models.IntegerField(choices=[(1, 'Gas'), (2, 'Electric'), (3, 'Temperature'), (4, 'Prediction')], default=1),
            preserve_default=False,
        ),
    ]
