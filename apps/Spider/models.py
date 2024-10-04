from pathlib import Path
from uuid import uuid4

from django.db import models
import shutil


class SpiderModel(models.Model):
    """
    爬虫模型
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True, verbose_name='爬虫名')
    spiderUid = models.UUIDField(null=False, unique=True, verbose_name='爬虫唯一标识')
    resources = models.CharField(max_length=100, unique=True, verbose_name='爬虫资源路径')
    founder = models.ForeignKey('User.UserModel', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='创建人')
    status = models.BooleanField(default=True, verbose_name='爬虫状态')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def delete(self, using=None, keep_parents=False):
        if Path(self.resources).exists():
            shutil.rmtree(self.resources)
        return super().delete(using, keep_parents)
