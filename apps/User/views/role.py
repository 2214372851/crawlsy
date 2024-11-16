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
    pagination_class = None

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        return filter_data


router = routers.DefaultRouter()
router.register('role', RoleViewSet, basename='role')
router.register('role-option', RoleOptionViewSet, basename='roleOption')
