# Generated by Django 2.2.7 on 2019-12-13 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_reply_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply_to',
        ),
    ]