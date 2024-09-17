from rest_framework import serializers

from apps.Node.models import NodeModel


class NodeSerializer(serializers.ModelSerializer):
    """
    节点序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = NodeModel
        fields = '__all__'
