# Generated by Django 3.0.5 on 2020-06-10 22:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_auto_20200610_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='availible_day_player',
            name='sport_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Team'),
        ),
        migrations.AlterField(
            model_name='noticing',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 11, 6, 29, 44, 66954)),
        ),
        migrations.AlterField(
            model_name='training',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 11, 6, 29, 44, 54026)),
        ),
        migrations.AlterField(
            model_name='voting',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 11, 6, 29, 44, 55018)),
        ),
    ]
