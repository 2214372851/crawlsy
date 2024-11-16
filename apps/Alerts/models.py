from django.db import models


class AlertRuleModel(models.Model):
    """
    告警规则
    """
    name = models.CharField(max_length=50, verbose_name='规则名称', unique=True)
    description = models.TextField(verbose_name='描述')
    mertric = models.CharField(max_length=50, verbose_name='监控指标')
    condition = models.CharField(max_length=50, verbose_name='监控条件')
    threshold = models.FloatField(verbose_name='阈值')
    severity_choices = (
        ('critical', '严重'),
        ('warning', '警告'),
        ('info', '提示'),
    )
    severity = models.CharField(max_length=10, choices=severity_choices, verbose_name='告警级别')
    target = models.ManyToManyField('User.UserModel', related_name='alert_target', blank=True, verbose_name='告警对象')
    status = models.BooleanField(default=True, verbose_name='状态')
    feishuWebhook = models.CharField(max_length=255, null=True, blank=True, verbose_name='飞书webhook')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    interval = models.IntegerField(default=60, verbose_name='告警间隔')
    lastTriggerTime = models.DateTimeField(null=True, blank=True, verbose_name='上次触发时间')

    class Meta:
        db_table = 'alertRule'
        ordering = ['-createTime']
        verbose_name = '告警规则'
        verbose_name_plural = verbose_name


class AlertRecordModel(models.Model):
    """
    告警记录
    """
    alertRule = models.ForeignKey('AlertRuleModel', on_delete=models.CASCADE, verbose_name='告警规则')
    metric = models.CharField(max_length=50, verbose_name='监控指标')
    value = models.FloatField(verbose_name='监控值')
    triggerTime = models.DateTimeField(verbose_name='触发时间')

    class Meta:
        db_table = 'alertRecord'
        ordering = ['-triggerTime']
        verbose_name = '告警记录'
        verbose_name_plural = verbose_name
