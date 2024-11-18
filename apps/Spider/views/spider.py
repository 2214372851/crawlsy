"""
记录爬虫的基本信息
"""
from uuid import uuid4

from rest_framework import routers
from rest_framework.views import Request, APIView
from django.http import FileResponse
from apps.Spider.models import SpiderModel
from apps.Task.models import TaskModel
from utils.code import Code
from utils.response import CustomResponse
from utils.unzip import zip
from apps.Spider.serializer import SpiderSerializer, SpiderOptionSerializer, SpiderTaskSerializer
from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin, CustomRetrieveMixin
from django.conf import settings


class SpiderViewSet(CustomModelViewSet):
    queryset = SpiderModel.objects.all()
    serializer_class = SpiderSerializer
    lookup_field = 'id'

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request: Request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        spider_uid = uuid4()
        request.data['spiderUid'] = spider_uid
        resources = settings.IDE_RESOURCES / str(spider_uid)
        resources.mkdir(parents=True)
        request.data['resources'] = str(resources)
        request.data['founder'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if 'founder' in request.data:
            del request.data['founder']
        if 'spiderUid' in request.data:
            del request.data['spiderUid']
        if 'resources' in request.data:
            del request.data['resources']
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        founder = self.request.query_params.get('founder', None)
        spiderUid = self.request.query_params.get('spiderUid', None)
        status = self.request.query_params.get('status', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        if founder: filter_data = filter_data.filter(founder__username__icontains=founder)
        if spiderUid: filter_data = filter_data.filter(spiderUid=spiderUid)
        if status: filter_data = filter_data.filter(status=status == 'true')
        return filter_data


class SpiderOptionViewSet(CustomGenericViewSet, CustomListMixin):
    queryset = SpiderModel.objects.all()
    serializer_class = SpiderOptionSerializer
    lookup_field = 'id'
    pagination_class = None

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        filter_data = filter_data.filter(status=True)
        return filter_data


class SpiderTaskViewSet(CustomGenericViewSet, CustomRetrieveMixin):
    queryset = SpiderModel.objects.all()
    serializer_class = SpiderTaskSerializer
    lookup_field = 'id'
    pagination_class = None

    def retrieve(self, request: Request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        return queryset


class SpiderPullView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request: Request):
        task_uid = request.query_params.get('taskUid')
        secret_key = request.META.get('HTTP_SECRET')
        if not secret_key:
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg='未携带身份信息'
            )
        if not task_uid:
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg='参数错误'
            )
        if secret_key != settings.SECRET_KEY:
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg='身份信息错误'
            )
        task = TaskModel.objects.filter(taskUid=task_uid).first()
        if not task:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='任务不存在'
            )
        spider_uid = str(task.taskSpider.spiderUid)
        project_path = settings.IDE_RESOURCES / spider_uid
        if not project_path.exists():
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='爬虫数据不存在'
            )
        temp_path = settings.IDE_TEMP / f'{spider_uid}.zip'
        temp_path.parent.mkdir(exist_ok=True, parents=True)
        zip(file_path=project_path, zip_filename=temp_path)
        if temp_path.stat().st_size > settings.IDE_MAX_FILE_SIZE:
            return CustomResponse(
                code=Code.FAILED_PRECONDITION,
                msg='文件过大超过阈值'
            )
        zip_file = open(temp_path, 'rb')
        response = FileResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={spider_uid}.zip'
        return response


router = routers.DefaultRouter()
router.register('spider', SpiderViewSet, basename='spider')
router.register('spider-task', SpiderTaskViewSet, basename='spiderTask')
router.register('spider-option', SpiderOptionViewSet, basename='spiderOption')
