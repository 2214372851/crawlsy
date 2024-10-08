from rest_framework import serializers
from apps.Spider.models import SpiderModel
from apps.Task.serializer import TaskRelatedSerializers


class SpiderSerializer(serializers.ModelSerializer):
    founderUser = serializers.SerializerMethodField(read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    def get_founderUser(self, obj: SpiderModel):
        user = obj.founder
        return {
            'uid': user.uid,
            'username': user.username
        }

    class Meta:
        model = SpiderModel
        fields = '__all__'
        extra_kwargs = {
            'founder': {'write_only': True},
            'resources': {'write_only': True},
        }


class SpiderTaskSerializer(SpiderSerializer):
    taskmodel_set = TaskRelatedSerializers(read_only=True, many=True)


class SpiderOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiderModel
        fields = ('id', 'name')
