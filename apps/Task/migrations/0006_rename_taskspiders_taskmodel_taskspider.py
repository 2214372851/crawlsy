# Generated by Django 4.2.1 on 2024-08-24 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0005_taskmodel_taskspiders'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskmodel',
            old_name='taskSpiders',
            new_name='taskSpider',
        ),
    ]
