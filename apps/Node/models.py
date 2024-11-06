from django.core.exceptions import ValidationError
from django.db import models


class NodeModel(models.Model):
    """
    节点模型
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True, verbose_name='节点名')
    nodeUid = models.UUIDField(null=False, unique=True, verbose_name='节点唯一标识')
    status = models.BooleanField(default=True, verbose_name='节点状态')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_value = NodeModel.objects.get(pk=self.pk).nodeUid
            if self.nodeUid != old_value:
                raise ValidationError("This field node_uid cannot be modified.")
        super(NodeModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'node'
        ordering = ['-createTime']
        verbose_name = '节点'
        verbose_name_plural = verbose_name
