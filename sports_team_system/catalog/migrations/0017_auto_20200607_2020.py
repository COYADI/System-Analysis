# Generated by Django 3.0.5 on 2020-06-07 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200607_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting',
            name='expire_time',
        ),
        migrations.AlterField(
            model_name='noticing',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 7, 20, 20, 54, 718287)),
        ),
        migrations.AlterField(
            model_name='training',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 7, 20, 20, 54, 714295)),
        ),
        migrations.AlterField(
            model_name='voting',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 7, 20, 20, 54, 717283)),
        ),
    ]