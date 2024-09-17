from rest_framework import serializers
from apps.Spider.models import SpiderModel


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
            'status': {'read_only': True},
        }
