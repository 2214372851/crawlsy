# Generated by Django 4.2.1 on 2024-08-24 07:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Spider', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spidermodel',
            name='nodeUid',
        ),
        migrations.AddField(
            model_name='spidermodel',
            name='spiderUid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='爬虫唯一标识'),
        ),
        migrations.AlterField(
            model_name='spidermodel',
            name='status',
            field=models.BooleanField(default=True, verbose_name='爬虫状态'),
        ),
    ]
