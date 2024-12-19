# Generated by Django 4.2.1 on 2024-12-03 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_usermodel_feishu_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOperationLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('operation_type', models.CharField(max_length=32, verbose_name='操作类型')),
                ('description', models.TextField(verbose_name='操作描述')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP地址')),
                ('operation_time', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('status', models.BooleanField(default=True, verbose_name='操作结果')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.usermodel', verbose_name='操作用户')),
            ],
            options={
                'verbose_name': '用户操作日志',
                'verbose_name_plural': '用户操作日志',
                'db_table': 'user_operation_log',
                'ordering': ['-operation_time'],
            },
        ),
    ]
