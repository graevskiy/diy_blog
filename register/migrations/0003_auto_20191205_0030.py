# Generated by Django 2.2.7 on 2019-12-04 21:30

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20191126_2346'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_author',
            field=models.BooleanField(default=False),
        ),
    ]
