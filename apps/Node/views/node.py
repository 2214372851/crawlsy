"""
唯一识别根据redis中 keys * 值添加在线节点， 子节点每60s同步一次状态
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers
from rest_framework.views import Request

from apps.Node.models import NodeModel
from apps.Node.serializer import NodeSerializer
from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin


class NodeViewSet(CustomModelViewSet):
    """
    节点管理视图集
    """
    queryset = NodeModel.objects.all()
    serializer_class = NodeSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary='节点列表',
        operation_description='节点列表',
        manual_parameters=[
            openapi.Parameter(
                'orderBy',
                openapi.IN_QUERY,
                description='排序, 默认为创建时间的倒序(-createTime)',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='节点名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'nodeUid',
                openapi.IN_QUERY,
                description='节点UID搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description='状态搜索(true|false)',
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        tags=['节点管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "total": 1,
                            "list": [
                                {
                                    "id": 2,
                                    "createTime": "2024-08-16 21:06:40",
                                    "updateTime": "2024-08-16 21:06:40",
                                    "name": "测试节点1",
                                    "nodeUid": "3d10d024-56e3-4d79-b417-53d2bef3b504",
                                    "status": False
                                }
                            ]
                        }
                    }
                })
        }
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='节点详情',
        operation_description='节点详情',
        tags=['节点管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "id": 2,
                            "createTime": "2024-08-16 21:06:40",
                            "updateTime": "2024-08-16 21:16:20",
                            "name": "string",
                            "nodeUid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "status": True
                        }
                    }
                })
        }
    )
    def retrieve(self, request: Request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='创建节点',
        operation_description='创建节点',
        manual_parameters=[],
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['name', 'nodeUid'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='节点名'),
                'nodeUid': openapi.Schema(type=openapi.TYPE_STRING, description='节点标识')
            }
        ),
        tags=['节点管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "id": 3,
                            "createTime": "2024-08-16 21:21:38",
                            "updateTime": "2024-08-16 21:21:38",
                            "name": "测试节点2",
                            "nodeUid": "787237b3-f59e-4aa3-9eba-7d98f122b6d5",
                            "status": True
                        }
                    }
                })
        }
    )
    def create(self, request, *args, **kwargs):
        # TODO: 检查节点可用性
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='节点修改',
        operation_description='节点更新',
        tags=['节点管理'],
        manual_parameters=[
            openapi.Parameter(
                'partial',
                openapi.IN_QUERY,
                description='是否部分字段校验,默认为0全字段校验(0|1)',
                type=openapi.TYPE_STRING
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='节点名'),
            }
        ),
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "id": 2,
                            "createTime": "2024-08-16 21:06:40",
                            "updateTime": "2024-08-16 21:22:54",
                            "name": "测试节点 修改名称",
                            "nodeUid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "status": True
                        }
                    }
                })
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='节点删除',
        operation_description='删除节点',
        tags=['节点管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success"
                    }
                })
        }
    )
    def destroy(self, request, *args, **kwargs):
        # TODO：删除节点前，检查节点下是否有任务
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
    serializer_class = NodeSerializer
    lookup_field = 'id'
    pagination_class = None

    @swagger_auto_schema(
        operation_summary='节点选项列表',
        operation_description='节点选项列表',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='节点名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['节点管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "total": 1,
                            "list": [
                                {
                                    "id": 2,
                                    "name": "测试节点1"
                                }
                            ]
                        }
                    }
                })
        }
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        return filter_data


router = routers.DefaultRouter()
router.register('node', NodeViewSet, basename='node')
router.register('nodeOption', NodeOptionViewSet, basename='node-option')
