from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers
from rest_framework.views import Request

from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin
from ..models import PermissionModel
from ..serializer import PermissionSerializer, PermissionOptionSerializer


class PermissionViewSet(CustomModelViewSet):
    """
    权限视图集
    """
    queryset = PermissionModel.objects.all()
    serializer_class = PermissionSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary='权限列表',
        operation_description='权限列表',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='权限名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['权限管理'],
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='权限详情',
        operation_description='权限详情',
        tags=['权限管理'],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='权限创建',
        operation_description='权限创建',
        manual_parameters=[],
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['name', 'method', 'path'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='权限名'),
                'method': openapi.Schema(type=openapi.TYPE_STRING, enum=['GET', 'POST', 'PUT', 'DELETE'],
                                         description='权限方法'),
                'path': openapi.Schema(type=openapi.TYPE_STRING, description='路径'),
                'menu': openapi.Schema(type=openapi.TYPE_INTEGER, description='菜单ID'),
            }
        ),
        tags=['权限管理'],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='权限修改',
        operation_description='权限信息更新',
        tags=['权限管理'],
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
            required=['name', 'method', 'path'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='权限名'),
                'method': openapi.Schema(type=openapi.TYPE_STRING, enum=['GET', 'POST', 'PUT', 'DELETE'],
                                         description='权限方法'),
                'path': openapi.Schema(type=openapi.TYPE_STRING, description='路径'),
                'menu': openapi.Schema(type=openapi.TYPE_INTEGER, description='菜单ID'),
            }
        )
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='权限删除',
        operation_description='权限删除',
        tags=['权限管理'],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        method = self.request.query_params.get('method', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        if method: filter_data = filter_data.filter(method=method)
        return filter_data


class PermissionOptionViewSet(CustomGenericViewSet, CustomListMixin):
    queryset = PermissionModel.objects.all()
    serializer_class = PermissionOptionSerializer
    lookup_field = 'id'
    pagination_class = None

    @swagger_auto_schema(
        operation_summary='权限选项列表',
        operation_description='权限选项列表',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='权限名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['权限管理'],
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        return filter_data


router = routers.DefaultRouter()
router.register('permission', PermissionViewSet, basename='permission')
router.register('permission-option', PermissionOptionViewSet, basename='permission-option')
