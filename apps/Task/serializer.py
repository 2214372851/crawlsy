from rest_framework import serializers
from apps.Task.models import TaskModel
from utils.date import validate_cron


class TaskSerializers(serializers.ModelSerializer):
    """
    任务序列化器
    """
    nodes = serializers.SerializerMethodField(read_only=True)
    founderUser = serializers.SerializerMethodField(read_only=True)
    spider = serializers.SerializerMethodField(read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    def get_nodes(self, obj: TaskModel):
        return [
            {
                'id': i.id,
                'nodeUid': i.nodeUid,
                'name': i.name,
                'status': i.status,
            }
            for i in obj.taskNodes.all()
        ]

    def get_spider(self, obj: TaskModel):
        return {
            'id': obj.taskSpider.id,
            'spiderUid': obj.taskSpider.spiderUid,
            'name': obj.taskSpider.name,
            'status': obj.taskSpider.status,
        }

    def get_founderUser(self, obj: TaskModel):
        user = obj.founder
        return {
            'uid': user.uid,
            'username': user.username
        }

    def validate(self, attrs):
        if attrs['isTiming']:
            if not attrs['cronExpression']:
                raise serializers.ValidationError(
                    {'cronExpression': '定时任务的cron表达式不能为空'})
            if not validate_cron(attrs['cronExpression']):
                raise serializers.ValidationError(
                    {'cronExpression': 'cron表达式不符合规范'})
        return attrs

    class Meta:
        model = TaskModel
        fields = '__all__'
        extra_kwargs = {
            'taskNodes': {'write_only': True},
            'founder': {'write_only': True},
            'taskSpider': {'write_only': True},
            'status': {'read_only': True},
        }
