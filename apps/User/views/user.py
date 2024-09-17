from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers
from rest_framework.views import Request

from utils.viewset import CustomModelViewSet
from apps.User.models import UserModel
from apps.User.serializer import UserSerializer


class UserViewSet(CustomModelViewSet):
    """
    用户视图集
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary='用户列表',
        operation_description='用户列表',
        manual_parameters=[
            openapi.Parameter(
                'orderBy',
                openapi.IN_QUERY,
                description='排序, 默认为创建时间的倒序(-createTime)',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                description='用户名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description='邮箱号称模糊搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description='状态搜索(true|false)',
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        tags=['用户管理'],
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
                                    "createTime": "2024-07-07 14:08:03",
                                    "updateTime": "2024-07-07 14:08:03",
                                    "role": [
                                        {
                                            "name": "管理员",
                                            "id": 1
                                        }
                                    ],
                                    "uid": "109cd8415dfa4f69aa6c2d7e9f73c383",
                                    "username": "超级管理员",
                                    "email": "bybxbwg@foxmail.com",
                                    "status": True,
                                    "lastLoginTime": "2024-07-07T14:08:03+08:00"
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
        operation_summary='用户详情',
        operation_description='用户详情',
        tags=['用户管理'],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='创建用户',
        operation_description='创建用户',
        manual_parameters=[],
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['username', 'password', 'email'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
                'role': openapi.Schema(type=openapi.TYPE_ARRAY,
                                       items=openapi.Schema('身份组', type=openapi.TYPE_INTEGER),
                                       description='身份组ID'),
            }
        ),
        tags=['用户管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "createTime": "2024-04-24 10:55:49",
                            "updateTime": "2024-04-24 10:55:49",
                            "group": [],
                            "uid": "92688660-1089-4e90-9293-48389849f516",
                            "username": "yunhai",
                            "phone": "15924817361",
                            "email": "bybxbwx@foxmail.com",
                            "state": 2
                        }
                    }
                })
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='用户修改',
        operation_description='用户信息更新',
        tags=['用户管理'],
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
            required=['username', 'password', 'email'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='邮箱'),
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='账号状态'),
                'role': openapi.Schema(type=openapi.TYPE_ARRAY,
                                       items=openapi.Schema('身份组', type=openapi.TYPE_INTEGER),
                                       description='身份组ID'),
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
                            "createTime": "2024-04-23 17:53:31",
                            "updateTime": "2024-04-23 17:53:31",
                            "group": [],
                            "uid": "37fd8d53-137c-4fa1-a20b-fdd5ba6c1a2a",
                            "username": "admin",
                            "phone": "15924817362",
                            "email": "bybxbwg@foxmail.com",
                            "state": 1
                        }
                    }
                })
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='用户删除',
        operation_description='删除用户',
        tags=['用户管理'],
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
        return super().destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        username = self.request.query_params.get('username', None)
        email = self.request.query_params.get('email', None)
        status = self.request.query_params.get('status', None)
        if username: filter_data = filter_data.filter(username__icontains=username)
        if email: filter_data = filter_data.filter(email__icontains=email)
        if status in {'true', 'false'}: filter_data = filter_data.filter(status=True if status == 'true' else False)
        return filter_data


router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
