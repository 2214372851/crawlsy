from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from utils.code import Code
from utils.response import CustomResponse
from utils.token import login_token, remove_token, refresh_access_token
from apps.User.models import UserModel
from django.db.models import QuerySet


class LoginView(APIView):
    """
    登录视图
    """

    @swagger_auto_schema(
        operation_summary='用户登录',
        operation_description='输入邮箱或手机号与密码进行登录',
        tags=['登录'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['account', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='账号'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码')
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
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTM5ODI3NzYsImlhdCI6MTcxMzk3OTE3NiwiaXNzIjoiU3BpZGVyU3R1ZGlvLUlTU0AyMDI0IiwiZGF0YSI6eyJ1c2VyX2d1aWQiOiIzN2ZkOGQ1My0xMzdjLTRmYTEtYTIwYi1mZGQ1YmE2YzFhMmEifX0.F7C29xq33r-a4QXULFHy2ZUeGReBT_vHf_YkpYa88Lw",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQwNjU1NzYsImlhdCI6MTcxMzk3OTE3NiwiaXNzIjoiU3BpZGVyU3R1ZGlvLUlTU0AyMDI0IiwiZGF0YSI6eyJ1c2VyX2d1aWQiOiIzN2ZkOGQ1My0xMzdjLTRmYTEtYTIwYi1mZGQ1YmE2YzFhMmEifX0.0BM9BrKn_IBf4BiPlEWkXeINYwwJ--vGnxaxb8wNOHU",
                            "username": "admin"
                        }
                    }
                })
        }
    )
    def post(self, request: Request):
        email, password = request.data.get('email'), request.data.get('password')
        if not UserModel.objects.filter(email=email).exists():
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg='账号或密码错误')
        user: UserModel = UserModel.objects.prefetch_related('role__permissions__menu').get(email=email)
        if not user.check_password(password):
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg='账号或密码错误')
        if not user.status:
            return CustomResponse(code=Code.PERMISSION_DENIED, msg='账号已被禁用')
        menus = {}
        permissions = {}
        for role in user.role.all():
            for permission in role.permissions.all():
                menus[permission.menu.id] = {
                    'id': permission.menu.id,
                    'name': permission.menu.name,
                    'path': permission.menu.path,
                    'icon': permission.menu.icon,
                    'parent': permission.menu.parent.id if permission.menu.parent else None
                }
                if permission.path not in permissions:
                    permissions[permission.path] = []
                if permission.method in permissions[permission.path]:
                    continue
                permissions[permission.path].append(permission.method)
        access_token, refresh_token = login_token(user)
        return CustomResponse(
            code=Code.OK,
            msg='登录成功',
            data={
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'lastLoginTime': user.lastLoginTime.strftime('%Y-%m-%d %H:%M:%S'),
                'username': user.username,
                'permissions': permissions,
                'menus': menus.values(),
                'role': user.role.all().values('id', 'name')
            }
        )


class LogoutView(APIView):
    """
    注销视图
    """

    @swagger_auto_schema(
        operation_summary='用户注销',
        operation_description='注销当前登录用户',
        tags=['登录'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "注销成功"
                    }
                })
        }
    )
    def get(self, request: Request):
        remove_token(request.META.get('HTTP_TOKEN'))
        return CustomResponse(code=Code.OK, msg='注销成功')


class RefreshTokenView(APIView):
    """
    无感刷新 Token 视图
    """

    @swagger_auto_schema(
        operation_summary='刷新身份信息',
        operation_description='根据 refresh token 刷新 access token',
        tags=['登录'],
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
    def get(self, request):
        print(request.META)
        access_token = refresh_access_token(request.META.get('HTTP_REFRESH_TOKEN'))
        if not access_token:
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg='身份信息过期')
        return CustomResponse(code=Code.OK, msg='Success', data={'accessToken': access_token})
