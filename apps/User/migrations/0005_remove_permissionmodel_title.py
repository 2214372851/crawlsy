# Generated by Django 4.2.1 on 2024-07-07 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_alter_usermodel_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permissionmodel',
            name='title',
        ),
    ]
