from django.db import close_old_connections
from django.db.models import Prefetch
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from apps.User.models import UserModel, PermissionModel
from utils.token import verify_token
from rest_framework.request import Request


class CustomLoginAuth(BaseAuthentication):

    def authenticate(self, request: Request):
        token = request.META.get('HTTP_TOKEN')
        refresh = False
        if request.resolver_match.url_name == 'refresh':
            token = request.META.get('HTTP_REFRESHTOKEN')
            refresh = True
        if not token:
            raise NotAuthenticated(detail='未携带身份信息')
        uid = verify_token(token, refresh)
        if not uid:
            raise NotAuthenticated(detail='身份信息不合法')

        user: UserModel = UserModel.objects.filter(uid=uid).first()
        if not user:
            raise NotAuthenticated(detail='当前用户不存在')
        if user.is_root:
            return user, token
        if user.status != 1:
            raise PermissionDenied(detail='用户不可用')
        return user, token


class CustomPermission(BasePermission):

    @staticmethod
    def _get_route_key(url_name, method):
        route_str = url_name.split('-')
        if len(route_str) < 2:
            return url_name
        view_name, api_name = route_str
        if api_name == 'detail' and method == 'PUT':
            return '{}-{}'.format(view_name, 'update')
        elif api_name == 'list' and method == 'POST':
            return '{}-{}'.format(view_name, 'create')
        elif api_name == 'detail' and method == 'DELETE':
            return '{}-{}'.format(view_name, 'delete')
        else:
            return url_name

    def has_permission(self, request, view):
        if request.user.is_root:
            return True
        request_path = self._get_route_key(request.resolver_match.url_name, request.method)
        prefetch = Prefetch(
            'permissions',
            queryset=PermissionModel.objects.filter(path=request_path, method=request.method),
            to_attr='filtered_permissions'
        )
        roles = request.user.role.prefetch_related(prefetch).all()
        for role in roles:
            if role.filtered_permissions:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # print(request.resolver_match.url_name, view.name, view.action, 'has_permission')
        return True


class WsAuthMiddleware:
    """
    自定义websocket认证
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        token = scope['query_string']
        token = token.decode('utf-8')
        if not token: return None
        try:
            uid = verify_token(token)
        except Exception:
            await send({"type": "websocket.accept"})
            error_message = {
                "type": "websocket.send",
                "text": '[身份信息校验失败]'
            }
            await send(error_message)
            close_message = {
                "type": "websocket.close",
                "code": 4002
            }
            await send(close_message)
            return None
        if not uid:
            return None
        return await self.inner(scope, receive, send)
