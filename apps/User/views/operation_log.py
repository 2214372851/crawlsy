from rest_framework import routers
from rest_framework.views import Request

from utils.viewset import (
    CustomGenericViewSet,
    CustomListMixin,
    CustomDestroyMixin,
)
from utils.code import Code
from utils.response import CustomResponse
from ..models import UserOperationLog
from ..serializer import UserOperationLogSerializer


class UserOperationViewSet(
    CustomGenericViewSet,
    CustomListMixin,
    CustomDestroyMixin,
):
    """
    用户操作日志视图集
    """

    queryset = UserOperationLog.objects.all()
    serializer_class = UserOperationLogSerializer
    lookup_field = "id"
    permission_classes = []

    def list(self, request: Request, *args, **kwargs):
        order_by = request.query_params.get("orderBy", "-operation_time")
        queryset = self.filter_queryset(self.get_queryset()).order_by(order_by)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(
            data={"total": queryset.count(), "list": serializer.data},
            msg="Success",
            code=Code.OK,
        )

    def filter_queryset(self, queryset):
        filter_data = queryset
        # 按操作类型筛选
        operation_type = self.request.query_params.get("operation_type", None)
        if operation_type:
            filter_data = filter_data.filter(operation_type__icontains=operation_type)

        # 按用户筛选
        username = self.request.query_params.get("username", None)
        if username:
            filter_data = filter_data.filter(user__username__icontains=username)

        return filter_data


router = routers.DefaultRouter()
router.register("operation", UserOperationViewSet, basename="operation")
