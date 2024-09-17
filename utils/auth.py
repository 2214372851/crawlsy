from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from apps.User.models import UserModel
from utils.token import verify_token
from rest_framework.request import Request


class CustomLoginAuth(BaseAuthentication):

    def authenticate(self, request: Request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise NotAuthenticated(detail='未携带身份信息')
        uid = verify_token(token)
        if not uid:
            raise NotAuthenticated(detail='身份信息不合法')

        user = UserModel.objects.filter(uid=uid).first()
        if not user:
            raise NotAuthenticated(detail='当前用户不存在')
        if user.state != 1:
            raise PermissionDenied(detail='用户不可用')

        return user, token


class CustomPermission(BasePermission):

    def _get_route_key(self, url_name, method):
        view_name, api_name = url_name.split('-')
        if api_name == 'detail' and method == 'PUT':
            return '{}-{}'.format(view_name, 'update')
        elif api_name == 'list' and method == 'POST':
            return '{}-{}'.format(view_name, 'create')
        elif api_name == 'detail' and method == 'DELETE':
            return '{}-{}'.format(view_name, 'delete')
        else:
            return url_name

    def has_permission(self, request, view):
        route_keys = {perm.key for group in request.user.group.filter(state=1) for perm in
                      group.permissions.all()}
        return self._get_route_key(request.resolver_match.url_name, request.method) in route_keys

    def has_object_permission(self, request, view, obj):
        # print(request.resolver_match.url_name, view.name, view.action, 'has_permission')

        return True
