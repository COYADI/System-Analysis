# Generated by Django 3.0.5 on 2020-05-18 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20200518_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='student_id',
        ),
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]