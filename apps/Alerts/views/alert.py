from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import routers
from rest_framework.views import Request, APIView

from utils.code import Code
from utils.feishu import FeishuApi
from utils.response import CustomResponse
from utils.viewset import CustomModelViewSet, CustomListMixin, CustomGenericViewSet
from ..models import AlertRuleModel, AlertRecordModel
from ..serializer import AlertSerializer, AlertRecordSerializer
from ...User.models import UserModel


class AlertViewSet(CustomModelViewSet):
    """
    告警视图集
    """
    queryset = AlertRuleModel.objects.all()
    serializer_class = AlertSerializer
    lookup_field = 'id'

    def list(self, request: Request, *args, **kwargs):
        """
        告警列表
        """
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
        severity = self.request.query_params.get('severity', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        if severity: filter_data = filter_data.filter(severity=severity)
        return filter_data


class AlertRecordViewSet(CustomGenericViewSet, CustomListMixin):
    queryset = AlertRecordModel.objects.all()
    serializer_class = AlertRecordSerializer
    lookup_field = 'id'

    def list(self, request: Request, *args, **kwargs):
        order_by = request.query_params.get('orderBy', '-triggerTime')
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

    def filter_queryset(self, queryset):
        filter_data = queryset
        alert = self.request.query_params.get('alert', None)
        if alert: filter_data = filter_data.filter(alertRule__id=alert)
        filter_data = filter_data
        return filter_data


class AlertTestApiView(APIView):

    def get(self, request: Request):
        alert_id = request.query_params.get('alert')
        if not alert_id:
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg='请输入告警内容')
        try:
            alert = AlertRuleModel.objects.prefetch_related('target').get(id=alert_id)
        except ObjectDoesNotExist:
            return CustomResponse(code=Code.NOT_FOUND, msg='告警不存在')
        users_feishu_id = list(alert.target.filter(feishu_id__isnull=False).values_list('feishu_id', flat=True))
        webhook_url = alert.feishuWebhook
        if not webhook_url and not users_feishu_id:
            return CustomResponse(code=Code.NOT_FOUND, msg='请配置飞书webhook或告警对象')
        feishu = FeishuApi(settings.APP_ID, settings.APP_SECRET)
        if users_feishu_id:
            feishu.send_message(
                users_id=users_feishu_id,
                msg=f'{alert.name}告警测试',
                severity=alert.severity,
                interval=alert.interval,
                callback_url=f'http://localhost:5173/alert/details?id={alert_id}',
                card_id=settings.CARD_ID,
                card_version=settings.CARD_VERSION
            )
        feishu.send_webhook(
            url=webhook_url,
            users_id=users_feishu_id,
            severity=alert.severity,
            interval=alert.interval,
            callback_url=f'http://localhost:5173/alert/details?id={alert_id}',
            card_id=settings.CARD_ID,
            card_version=settings.CARD_VERSION,
            msg=f'{alert.name}告警测试'

        )
        return CustomResponse(code=Code.OK, msg='Success')


router = routers.DefaultRouter()
router.register('alert', AlertViewSet, basename='alert')
router.register('alert-record', AlertRecordViewSet, basename='alertRecord')
