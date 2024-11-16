from django.db.models import Prefetch
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.User.models import UserModel, PermissionModel
from utils.code import Code
from utils.response import CustomResponse
from utils.token import login_token, remove_token, refresh_access_token


class LoginView(APIView):
    """
    登录视图
    """
    authentication_classes = []
    permission_classes = []

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
        prefetch = Prefetch(
            'permissions',
            queryset=PermissionModel.objects.select_related('menu', 'menu__parent').all(),
            to_attr='prefetched_permissions'
        )

        roles = user.role.prefetch_related(prefetch).all()

        def add_menu(item):
            if item.id not in menus:
                menus[item.id] = {
                    'id': item.id,
                    'name': item.name,
                    'path': item.path,
                    'icon': item.icon,
                    'parent': item.parent.id if item.parent else None
                }
                if item.parent:
                    add_menu(item.parent)

        for role in roles:
            for permission in role.prefetched_permissions:
                menu = permission.menu
                add_menu(menu)

                if permission.path not in permissions:
                    permissions[permission.path] = set()

                if permission.method not in permissions[permission.path]:
                    permissions[permission.path].add(permission.method)

        for path in permissions:
            permissions[path] = list(permissions[path])
        access_token, refresh_token = login_token(user)
        user.update_login_time()
        return CustomResponse(
            code=Code.OK,
            msg='登录成功',
            data={
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'lastLoginTime': user.lastLoginTime.strftime('%Y-%m-%d %H:%M:%S'),
                'username': user.username,
                'email': user.email,
                'permissions': permissions,
                'menus': menus.values(),
                'role': user.role.all().values('id', 'name')
            }
        )


class LogoutView(APIView):
    """
    注销视图
    """
    permission_classes = []

    def get(self, request: Request):
        remove_token(request.META.get('HTTP_TOKEN'))
        return CustomResponse(code=Code.OK, msg='注销成功')


class RefreshTokenView(APIView):
    """
    无感刷新 Token 视图
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        access_token = refresh_access_token(request.META.get('HTTP_REFRESHTOKEN'))
        if not access_token:
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg='身份信息不合法')
        return CustomResponse(code=Code.OK, msg='Success', data={'accessToken': access_token})
