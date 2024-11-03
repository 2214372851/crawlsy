from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.settings import api_settings

from utils.code import Code
from utils.response import CustomResponse


class CustomGenericViewSet(viewsets.GenericViewSet):
    """
    基础视图集
    """
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    serializer_class = None
    queryset = None
    lookup_field = 'uid'

    def get_queryset(self):
        assert self.queryset is not None, 'queryset no value is assigned'
        return self.queryset if isinstance(self.queryset, QuerySet) else self.queryset.all()

    def filter_queryset(self, queryset):
        raise ImportError("重写filter_queryset方法")

    def get_object(self):
        field_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        return self.get_queryset().filter(**field_kwargs).first()


class CustomCreateMixin:
    """
    创建 Mixin
    """

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return CustomResponse(code=Code.OK, msg='Success', data=serializer.data)

    def perform_create(self, serializer):
        serializer.save()


class CustomRetrieveMixin:
    """
    详情 Mixin
    """

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        if not instance: return CustomResponse(code=Code.NOT_FOUND, msg='未找到该资源')
        serializer = self.get_serializer(instance)
        self.check_object_permissions(request, serializer)
        return CustomResponse(code=Code.OK, msg='Success', data=serializer.data)


class CustomDestroyMixin:
    """
    删除 Mixin
    """

    def destroy(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse(code=Code.OK, msg='Success')

    def perform_destroy(self, instance):
        instance.delete()


class CustomListMixin:
    """
    列表 Mixin
    """

    def list(self, request: Request, *args, **kwargs):
        order_by = request.query_params.get('orderBy', '-createTime')
        queryset = self.filter_queryset(self.get_queryset()).order_by(order_by)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(
            data={
                'total': queryset.count(),
                'list': serializer.data
            },
            msg='Success',
            code=Code.OK)


class CustomUpdateMixin:
    """
    更新 Mixin
    """

    def update(self, request: Request, *args, **kwargs):
        # 默认 partial 为 False，进行全字段校验
        partial = request.query_params.get('partial', False)
        instance = self.get_object()
        if not instance: return CustomResponse(code=Code.NOT_FOUND, msg='未找到该资源')
        serializer = self.get_serializer(instance, data=request.data, partial=bool(partial))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # 缓存已存在时，强制清空缓存
            instance._prefetched_objects_cache = {}

        return CustomResponse(code=Code.OK, msg='Success', data=serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CustomModelViewSet(CustomGenericViewSet, CustomListMixin,
                         CustomRetrieveMixin, CustomCreateMixin,
                         CustomUpdateMixin, CustomDestroyMixin):
    pass
