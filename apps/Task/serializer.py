import json
import logging

import pytz
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from rest_framework import serializers

from apps.Node.models import NodeModel
from apps.Task.models import TaskModel
from utils.date import validate_cron
from utils.node_stat import get_node_conn
from utils.status import Status

logger = logging.getLogger('django')


class TaskSerializers(serializers.ModelSerializer):
    """
    任务序列化器
    """
    founderUser = serializers.SerializerMethodField(read_only=True)
    spiderName = serializers.SerializerMethodField(read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    taskNodes = serializers.PrimaryKeyRelatedField(many=True, queryset=NodeModel.objects, required=False)

    def get_founderUser(self, obj: TaskModel):
        user = obj.founder
        return {
            'uid': user.uid,
            'username': user.username
        }

    def get_spiderName(self, obj: TaskModel):
        return obj.taskSpider.name

    def validate(self, attrs):
        if 'isTiming' not in attrs:
            raise serializers.ValidationError(
                {'isTiming': '请选择是否为定时任务'})
        elif attrs.get('isTiming'):
            if 'cronExpression' not in attrs:
                raise serializers.ValidationError(
                    {'cronExpression': '定时任务必须设置cron表达式'})
            if not attrs['cronExpression']:
                raise serializers.ValidationError(
                    {'cronExpression': '定时任务的cron表达式不能为空'})
            if not validate_cron(attrs['cronExpression']):
                raise serializers.ValidationError(
                    {'cronExpression': 'cron表达式不符合规范'})
        return attrs

    def update(self, instance: TaskModel, validated_data):
        if validated_data.get('status') and validated_data.get('isTiming'):
            PeriodicTask.objects.filter(name=instance.name).delete()
            # 解析 cron 表达式
            parts = validated_data['cronExpression'].split()
            minute, hour, day_of_month, month_of_year, day_of_week = parts
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_week=day_of_month,
                day_of_month=month_of_year,
                month_of_year=day_of_week,
                timezone=pytz.timezone('Asia/Shanghai')
            )
            PeriodicTask.objects.update_or_create(
                name=validated_data['name'],
                crontab=schedule,
                task='task_celery.node_status.tasks.task_start',
                args=json.dumps([str(instance.taskUid)]),
            )
            logger.info('定时任务创建成功')
        else:
            if instance.status and instance.isTiming:
                PeriodicTask.objects.filter(name=instance.name).delete()
                logger.info('定时任务删除成功')
        if instance.taskNodes.count() > 0 and [i.id for i in instance.taskNodes.all()] != list(
                validated_data['taskNodes']):
            conn = get_node_conn()
            flag = True
            for node in instance.taskNodes.all():
                service = conn.get(f"stat:{node.nodeUid}")
                if service is None: continue
                service = json.loads(service.decode('utf-8'))
                running_task = {i['taskUid']: i['status'] for i in service['tasks']}
                if running_task.get(str(instance.taskUid), Status.NOT_EXIST.value) != Status.NOT_EXIST.value:
                    flag = False
                    break
            if not flag:
                raise ValueError('节点仍在占用请先取消部署')

            logger.info('任务节点修改成功')
        return super().update(instance, validated_data)

    class Meta:
        model = TaskModel
        fields = '__all__'
        extra_kwargs = {
            'founder': {'write_only': True}
        }


# spider反查询序列化器
class TaskRelatedSerializers(TaskSerializers):
    """
    任务反查询序列化器
    """

    class Meta:
        model = TaskModel
        fields = ('id', 'name', 'status', 'isTiming', 'founderUser', 'createTime', 'updateTime')


class TaskDetailSerializers(TaskSerializers):
    """
    任务详情序列化器
    """
    taskNodes = serializers.SerializerMethodField(read_only=True)

    def get_taskNodes(self, obj: TaskModel):
        conn = get_node_conn()
        result = []
        for node in obj.taskNodes.all():
            service = conn.get(f"stat:{node.nodeUid}")
            if service is None:
                result.append({
                    'id': node.id,
                    'name': node.name,
                    'nodeUid': node.nodeUid,
                    'status': 16
                })
                continue
            service = json.loads(service.decode('utf-8'))
            running_task = {i['taskUid']: i['status'] for i in service['tasks']}
            result.append({
                'id': node.id,
                'name': node.name,
                'nodeUid': node.nodeUid,
                'status': running_task.get(str(obj.taskUid), Status.NOT_EXIST),
            })
        return result
