# Generated by Django 4.2.1 on 2024-11-16 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_alter_menumodel_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='feishu_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='飞书用户ID'),
        ),
    ]
