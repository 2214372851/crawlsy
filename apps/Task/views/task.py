"""
即时任务
    taskUid 由队列任务生成
    founder 由当前登录用户
    taskNodes 由节点列表选中
"""
from rest_framework import routers
from rest_framework.views import Request
from apps.Task.models import TaskModel
from apps.Task.serializer import TaskSerializers, TaskDetailSerializers
from utils.code import Code
from utils.response import CustomResponse
from utils.viewset import CustomModelViewSet


class TaskViewSet(CustomModelViewSet):
    """
    任务管理视图集
    """
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializers
    lookup_field = 'id'



    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        if not instance: return CustomResponse(code=Code.NOT_FOUND, msg='未找到该资源')
        serializer = TaskDetailSerializers(instance)
        self.check_object_permissions(request, serializer)
        return CustomResponse(code=Code.OK, msg='Success', data=serializer.data)


    def create(self, request, *args, **kwargs):
        request.data['founder'] = 1
        # request.data['founder'] = request.user.uid
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        if 'founder' in request.data:
            del request.data['founder']
        return super().update(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        # TODO: 检测并移除所有部署
        return super().destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        founder = self.request.query_params.get('founder', None)
        status = self.request.query_params.get('status', None)
        isTiming = self.request.query_params.get('isTiming', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        if founder: filter_data = filter_data.filter(founder__username__icontains=founder)
        if status: filter_data = filter_data.filter(status=status == 'true')
        if isTiming: filter_data = filter_data.filter(isTiming=isTiming == 'true')
        return filter_data


router = routers.DefaultRouter()
router.register('task', TaskViewSet, basename='task')
