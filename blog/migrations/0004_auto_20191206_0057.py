# Generated by Django 2.2.7 on 2019-12-05 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191205_0030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-pub_date', 'category'], 'permissions': [('can_add_posts', 'Can add Posts')]},
        ),
    ]
