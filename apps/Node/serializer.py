from rest_framework import serializers

from apps.Node.models import NodeModel


class NodeSerializer(serializers.ModelSerializer):
    """
    节点序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    def validate_nodeUid(self, value):
        if NodeModel.objects.filter(nodeUid=value).exists():
            raise serializers.ValidationError('节点已存在')
        if self.instance:
            return self.instance.nodeUid
        return value

    class Meta:
        model = NodeModel
        fields = '__all__'


class NodeOptionSerializer(serializers.ModelSerializer):
    """
    节点选项序列化器
    """

    class Meta:
        model = NodeModel
        fields = ('id', 'name')
