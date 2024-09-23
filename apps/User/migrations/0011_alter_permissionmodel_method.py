# Generated by Django 4.2.1 on 2024-07-07 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_alter_menumodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionmodel',
            name='method',
            field=models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], max_length=32, verbose_name='请求方法'),
        ),
    ]