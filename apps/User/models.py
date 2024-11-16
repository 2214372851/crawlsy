import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone


class UserModel(models.Model):
    """
    用户模型
    """
    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='用户唯一标识')
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=False, verbose_name='状态')
    lastLoginTime = models.DateTimeField(auto_now=True, verbose_name='最后登录时间')
    role = models.ManyToManyField('RoleModel', verbose_name='角色')
    feishu_id = models.CharField(max_length=32, null=True, blank=True, verbose_name='飞书用户ID')

    def check_password(self, password):
        return check_password(password, self.password)

    @staticmethod
    def make_password(password):
        return make_password(password)

    def update_login_time(self):
        self.lastLoginTime = timezone.now()
        self.save()

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-createTime']


class RoleModel(models.Model):
    """
    角色模型
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True, verbose_name='角色名')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    permissions = models.ManyToManyField('PermissionModel', verbose_name='权限')

    class Meta:
        db_table = 'role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['-createTime']


class PermissionModel(models.Model):
    """
    权限模型
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='权限名')
    method_choices = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    )
    method = models.CharField(max_length=32, choices=method_choices, verbose_name='请求方法')
    path = models.CharField(max_length=32, verbose_name='请求路径')
    menu = models.ForeignKey('MenuModel', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='菜单')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'permission'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['-createTime']
        unique_together = ('method', 'path',)


class MenuModel(models.Model):
    """
    菜单模型
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='菜单名')
    icon = models.CharField(max_length=32, verbose_name='图标')
    path = models.CharField(max_length=32, verbose_name='路径')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父菜单')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['-createTime']
        unique_together = ('name', 'path',)
