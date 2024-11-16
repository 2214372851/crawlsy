
from rest_framework import routers
from rest_framework.views import Request

from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin
from ..models import MenuModel
from ..serializer import MenuSerializer, MenuOptionSerializer


class MenuViewSet(CustomModelViewSet):
    """
    菜单管理视图集
    """
    queryset = MenuModel.objects.all()
    serializer_class = MenuSerializer
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


class MenuOptionViewSet(CustomGenericViewSet, CustomListMixin):
    queryset = MenuModel.objects.all()
    serializer_class = MenuOptionSerializer
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
router.register('menu', MenuViewSet, basename='menu')
router.register('menu-option', MenuOptionViewSet, basename='menuOption')
