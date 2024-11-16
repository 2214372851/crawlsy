from rest_framework import serializers
from .models import AlertRuleModel, AlertRecordModel


class AlertSerializer(serializers.ModelSerializer):
    """
    告警管理序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = AlertRuleModel
        fields = '__all__'
        read_only_fields = ('id',)


class AlertRecordSerializer(serializers.ModelSerializer):
    """
    告警记录序列化器
    """
    triggerTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = AlertRecordModel
        fields = '__all__'
        read_only_fields = ('id',)
