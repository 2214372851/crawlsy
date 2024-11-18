"""
唯一识别根据redis中 keys * 值添加在线节点， 子节点每60s同步一次状态
"""

from rest_framework import routers
from rest_framework.views import Request

from apps.Node.models import NodeModel
from apps.Node.serializer import NodeSerializer, NodeDetailSerializer, NodeOptionSerializer
from utils.code import Code
from utils.response import CustomResponse
from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin


class NodeViewSet(CustomModelViewSet):
    """
    节点管理视图集
    """
    queryset = NodeModel.objects.all()
    serializer_class = NodeSerializer
    lookup_field = 'id'

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        if not instance: return CustomResponse(code=Code.NOT_FOUND, msg='未找到该资源')
        serializer = NodeDetailSerializer(instance)
        self.check_object_permissions(request, serializer)
        return CustomResponse(code=Code.OK, msg='Success', data=serializer.data)

    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        status = self.request.query_params.get('status', None)
        nodeUid = self.request.query_params.get('nodeUid', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        if status: filter_data = filter_data.filter(status=status == 'true')
        if nodeUid: filter_data = filter_data.filter(nodeUid=nodeUid)
        return filter_data


class NodeOptionViewSet(CustomGenericViewSet, CustomListMixin):
    queryset = NodeModel.objects.all()
    serializer_class = NodeOptionSerializer
    lookup_field = 'id'
    pagination_class = None

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        filter_data = filter_data.filter(status=True)
        # TODO: 返回分数 和 节点状态
        return filter_data


router = routers.DefaultRouter()
router.register('node', NodeViewSet, basename='node')
router.register('node-option', NodeOptionViewSet, basename='nodeOption')
