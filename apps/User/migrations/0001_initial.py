# Generated by Django 4.2.1 on 2024-07-07 09:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='菜单名')),
                ('icon', models.CharField(max_length=32, verbose_name='图标')),
                ('path', models.CharField(max_length=32, verbose_name='请求路径')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='User.menumodel', verbose_name='父菜单')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
                'db_table': 'menu',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PermissionModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='权限名')),
                ('method', models.CharField(max_length=32, verbose_name='请求方法')),
                ('path', models.CharField(max_length=32, verbose_name='请求路径')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.menumodel', verbose_name='菜单')),
            ],
            options={
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
                'db_table': 'permission',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='角色名')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('permissions', models.ManyToManyField(to='User.permissionmodel', verbose_name='权限')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
                'db_table': 'role',
                'ordering': ['-createTime'],
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.CharField(default=uuid.UUID('c3a8ab2a-d975-414c-bcdb-254b556ef501'), max_length=32, unique=True, verbose_name='用户唯一标识')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.BooleanField(default=False, verbose_name='状态')),
                ('lastLoginTime', models.DateTimeField(auto_now=True, verbose_name='最后登录时间')),
                ('role', models.ManyToManyField(to='User.rolemodel', verbose_name='角色')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'user',
                'ordering': ['-createTime'],
            },
        ),
    ]