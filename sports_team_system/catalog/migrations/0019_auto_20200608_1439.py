# Generated by Django 3.0.6 on 2020-06-08 06:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20200607_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticing',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 8, 14, 39, 50, 767141)),
        ),
        migrations.AlterField(
            model_name='training',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 8, 14, 39, 50, 765146)),
        ),
        migrations.AlterField(
            model_name='voting',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 8, 14, 39, 50, 766144)),
        ),
    ]
