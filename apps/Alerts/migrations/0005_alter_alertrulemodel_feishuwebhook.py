# Generated by Django 4.2.1 on 2024-11-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alerts', '0004_alter_alertrulemodel_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertrulemodel',
            name='feishuWebhook',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='飞书webhook'),
        ),
    ]
