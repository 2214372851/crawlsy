from rest_framework import serializers
from apps.Task.models import TaskModel
from apps.Node.models import NodeModel
from utils.date import validate_cron


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

    class Meta:
        model = TaskModel
        fields = '__all__'
        extra_kwargs = {
            'founder': {'write_only': True},
            'status': {'read_only': True},
        }


# spider反查询序列化器
class TaskRelatedSerializers(TaskSerializers):
    """
    任务反查询序列化器
    """
    class Meta:
        model = TaskModel
        fields = ('id', 'name', 'status', 'isTiming', 'founderUser', 'createTime', 'updateTime')
