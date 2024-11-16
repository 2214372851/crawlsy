import shutil
from pathlib import Path

from django.db import models


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
    command = models.CharField(max_length=128, null=True, blank=True, verbose_name='启动命令')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def delete(self, using=None, keep_parents=False):
        if Path(self.resources).exists():
            shutil.rmtree(self.resources)
        return super().delete(using, keep_parents)

    class Meta:
        db_table = 'spider'
        ordering = ['-createTime']
        verbose_name = '爬虫'
        verbose_name_plural = verbose_name
