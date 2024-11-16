import json

from rest_framework import serializers

from apps.Node.models import NodeModel
from utils.node_stat import get_node_conn


class NodeSerializer(serializers.ModelSerializer):
    """
    节点序列化器
    """
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    nodeLoad = serializers.SerializerMethodField(read_only=True)

    def validate_nodeUid(self, value):
        if NodeModel.objects.filter(nodeUid=value).exists():
            raise serializers.ValidationError('节点已存在')
        if self.instance:
            return self.instance.nodeUid
        if get_node_conn().exists(f'stat:{value}'):
            return value
        raise serializers.ValidationError('节点不存在')

    def get_nodeLoad(self, obj: NodeModel):
        stat = get_node_conn().get(f'stat:{obj.nodeUid}')
        if not stat:
            return 0
        return json.loads(stat.decode('utf-8'))['load'][0]

    class Meta:
        model = NodeModel
        fields = '__all__'


class NodeDetailSerializer(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    monitor = serializers.SerializerMethodField(read_only=True)

    def get_monitor(self, obj: NodeModel):
        data = get_node_conn().lrange(f'monitor:{obj.nodeUid}', 0, 30)
        return [json.loads(item.decode('utf-8')) for item in data][::-1]

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
