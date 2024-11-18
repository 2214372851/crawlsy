from django.conf import settings
from rest_framework import routers
from rest_framework.views import Request, APIView

from apps.User.models import UserModel
from apps.User.serializer import UserSerializer, UserOptionSerializer
from utils.code import Code
from utils.feishu import FeishuApi
from utils.response import CustomResponse
from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin


class UserViewSet(CustomModelViewSet):
    """
    用户视图集
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

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


class UserOptionViewSet(CustomGenericViewSet, CustomListMixin):
    """
    角色视图集
    """
    queryset = UserModel.objects.all()
    serializer_class = UserOptionSerializer
    lookup_field = 'id'
    pagination_class = None

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        username = self.request.query_params.get('username', None)
        if username: filter_data = filter_data.filter(username__icontains=username)
        filter_data = filter_data
        return filter_data


class UserProfileApiView(APIView):
    permission_classes = []

    def get(self, request: Request):
        user = request.user
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data=UserSerializer(user).data,
        )


class UserFeishuView(APIView):
    permission_classes = []

    def get(self, request: Request):
        feishu = FeishuApi(settings.APP_ID, settings.APP_SECRET)
        result = feishu.get_users_id(request.user.email)[request.user.email]
        if not result:
            return CustomResponse(code=Code.NOT_FOUND, msg='请检查当前邮箱是否绑定飞书账号')
        request.user.feishu_id = result
        request.user.save()
        return CustomResponse(code=Code.OK, msg='Success')


router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('user-option', UserOptionViewSet, basename='userOption')
