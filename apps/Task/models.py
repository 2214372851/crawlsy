import uuid
from django.db import models


class TaskModel(models.Model):
    """
    任务模型
        存储节点ID
        存储定时器
    """
    id = models.AutoField(primary_key=True)
    taskUid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='任务唯一标识')
    name = models.CharField(max_length=32, unique=True, verbose_name='任务名')
    status = models.BooleanField(default=False, verbose_name='任务状态')
    founder = models.ForeignKey('User.UserModel', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='创建人')
    taskNodes = models.ManyToManyField('Node.NodeModel', verbose_name='任务节点')
    taskSpider = models.ForeignKey('Spider.SpiderModel', on_delete=models.PROTECT, verbose_name='任务爬虫')
    isTiming = models.BooleanField(default=False, verbose_name='是否定时')
    cronExpression = models.CharField(max_length=100, null=True, blank=True, verbose_name='定时任务cron表达式')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def delete(self, using=None, keep_parents=False):
        self.taskNodes.clear()
        super().delete()

    class Meta:
        db_table = 'task'
        ordering = ['-createTime']
        verbose_name = '任务'
        verbose_name_plural = verbose_name
