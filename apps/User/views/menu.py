from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers
from rest_framework.views import Request

from utils.viewset import CustomModelViewSet
from ..models import MenuModel
from ..serializer import MenuSerializer


class MenuViewSet(CustomModelViewSet):
    """
    菜单管理视图集
    """
    queryset = MenuModel.objects.all()
    serializer_class = MenuSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary='菜单列表',
        operation_description='菜单列表',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='菜单名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['菜单管理'],
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='菜单详情',
        operation_description='菜单详情',
        tags=['菜单管理'],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='菜单创建',
        operation_description='菜单创建',
        manual_parameters=[],
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['name', 'icon', 'path'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='菜单名'),
                'icon': openapi.Schema(type=openapi.TYPE_STRING, description='菜单图标'),
                'path': openapi.Schema(type=openapi.TYPE_STRING, description='菜单路径'),
                'parent': openapi.Schema(type=openapi.TYPE_INTEGER, description='菜单ID'),
            }
        ),
        tags=['菜单管理'],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='菜单修改',
        operation_description='菜单信息更新',
        tags=['菜单管理'],
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
            required=['name', 'icon', 'path'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='菜单名'),
                'icon': openapi.Schema(type=openapi.TYPE_STRING, description='菜单图标'),
                'path': openapi.Schema(type=openapi.TYPE_STRING, description='菜单路径'),
                'parent': openapi.Schema(type=openapi.TYPE_INTEGER, description='菜单ID'),
            }
        )
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='菜单删除',
        operation_description='菜单删除',
        tags=['菜单管理'],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        return filter_data


router = routers.DefaultRouter()
router.register('menu', MenuViewSet, basename='menu')
