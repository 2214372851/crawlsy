from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers
from rest_framework.views import Request

from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin
from ..models import RoleModel
from ..serializer import RoleSerializer


class RoleViewSet(CustomModelViewSet):
    """
    角色视图集
    """
    queryset = RoleModel.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary='角色列表',
        operation_description='角色列表',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='角色名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['角色管理'],
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='角色详情',
        operation_description='角色详情',
        tags=['角色管理'],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='角色创建',
        operation_description='角色创建',
        manual_parameters=[],
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['name'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='角色名'),
                'permissions': openapi.Schema(type=openapi.TYPE_ARRAY,
                                              items=openapi.Schema('权限组', type=openapi.TYPE_INTEGER),
                                              description='权限组ID'),
            }
        ),
        tags=['角色管理'],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='角色修改',
        operation_description='角色信息更新',
        tags=['角色管理'],
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
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='角色名'),
                'permissions': openapi.Schema(type=openapi.TYPE_ARRAY,
                                              items=openapi.Schema('权限组', type=openapi.TYPE_INTEGER),
                                              description='权限组ID'),
            }
        )
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='角色删除',
        operation_description='角色删除',
        tags=['角色管理'],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        return filter_data


class RoleOptionViewSet(CustomGenericViewSet, CustomListMixin):
    """
    角色视图集
    """
    queryset = RoleModel.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary='角色选项列表',
        operation_description='角色选项列表',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='角色名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['角色管理'],
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        return filter_data


router = routers.DefaultRouter()
router.register('role', RoleViewSet, basename='role')
router.register('roleOption', RoleOptionViewSet, basename='role-option')
