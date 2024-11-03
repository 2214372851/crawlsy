"""
即时任务
    taskUid 由队列任务生成
    founder 由当前登录用户
    taskNodes 由节点列表选中
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(
        operation_summary='任务列表',
        operation_description='任务列表',
        manual_parameters=[
            openapi.Parameter(
                'orderBy',
                openapi.IN_QUERY,
                description='排序, 默认为创建时间的倒序(-createTime)',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='任务名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'founder',
                openapi.IN_QUERY,
                description='创建人搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description='状态搜索(true|false)',
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'isTiming',
                openapi.IN_QUERY,
                description='是否定时搜索(true|false)',
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        tags=['任务管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "total": 1,
                            "list": [
                                {
                                    "id": 12,
                                    "nodes": [
                                        {
                                            "id": 2,
                                            "nodeUid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                            "name": "测试节点 修改名称",
                                            "status": False
                                        }
                                    ],
                                    "founderUser": {
                                        "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                        "username": "超级管理员"
                                    },
                                    "spider": {
                                        "id": 1,
                                        "spiderUid": "ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                                        "name": "测试爬虫0",
                                        "status": False
                                    },
                                    "createTime": "2024-08-24 16:11:56",
                                    "updateTime": "2024-08-24 16:11:56",
                                    "taskUid": "d3702283-16c7-472c-82f4-f66ba38e99df",
                                    "name": "测试任务1",
                                    "status": False,
                                    "isTiming": False,
                                    "cronExpression": ""
                                }
                            ]
                        }
                    }
                })
        }
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='任务详情',
        operation_description='任务详情',
        tags=['任务管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "id": 12,
                            "nodes": [
                                {
                                    "id": 2,
                                    "nodeUid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "name": "测试节点 修改名称",
                                    "status": False
                                }
                            ],
                            "founderUser": {
                                "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                "username": "超级管理员"
                            },
                            "spider": {
                                "id": 1,
                                "spiderUid": "ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                                "name": "测试爬虫0",
                                "status": False
                            },
                            "createTime": "2024-08-24 16:11:56",
                            "updateTime": "2024-08-24 16:11:56",
                            "taskUid": "d3702283-16c7-472c-82f4-f66ba38e99df",
                            "name": "测试任务1",
                            "status": False,
                            "isTiming": False,
                            "cronExpression": ""
                        }
                    }
                })
        }
    )
    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        if not instance: return CustomResponse(code=Code.NOT_FOUND, msg='未找到该资源')
        serializer = TaskDetailSerializers(instance)
        self.check_object_permissions(request, serializer)
        return CustomResponse(code=Code.OK, msg='Success', data=serializer.data)

    @swagger_auto_schema(
        operation_summary='创建任务',
        operation_description='创建任务',
        manual_parameters=[],
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['name', 'isTiming', 'cronExpression', 'taskNodes', 'taskSpider'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='任务名'),
                'taskSpider': openapi.Schema(type=openapi.TYPE_STRING, description='爬虫ID'),
                'isTiming': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='任务是否是定时任务'),
                'cronExpression': openapi.Schema(type=openapi.TYPE_STRING, description='定时任务corn表达式'),
                'taskNodes': openapi.Schema(type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_NUMBER,
                                                description='节点ID'
                                            ),
                                            description='调度节点')
            }
        ),
        tags=['任务管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "id": 12,
                            "nodes": [
                                {
                                    "id": 2,
                                    "nodeUid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "name": "测试节点 修改名称",
                                    "status": False
                                }
                            ],
                            "founderUser": {
                                "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                "username": "超级管理员"
                            },
                            "spider": {
                                "id": 1,
                                "spiderUid": "ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                                "name": "测试爬虫0",
                                "status": False
                            },
                            "createTime": "2024-08-24 16:11:56",
                            "updateTime": "2024-08-24 16:11:56",
                            "taskUid": "d3702283-16c7-472c-82f4-f66ba38e99df",
                            "name": "测试任务1",
                            "status": False,
                            "isTiming": False,
                            "cronExpression": ""
                        }
                    }
                })
        }
    )
    def create(self, request, *args, **kwargs):
        request.data['founder'] = 1
        # request.data['founder'] = request.user.uid
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='任务修改',
        operation_description='任务更新',
        tags=['任务管理'],
        manual_parameters=[
            openapi.Parameter(
                'partial',
                openapi.IN_QUERY,
                description='是否部分字段校验,默认为0全字段校验(0|1)',
                type=openapi.TYPE_STRING
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'cronExpression', 'isTiming', 'taskNodes', 'taskSpider'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='任务名'),
                'cronExpression': openapi.Schema(type=openapi.TYPE_STRING, description='cron表达式'),
                'taskSpider': openapi.Schema(type=openapi.TYPE_STRING, description='爬虫ID'),
                'isTiming': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='是否定时'),
                'taskNodes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_NUMBER, description='节点ID'),
                    description='任务节点'),
            }
        ),
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "code": 0,
                            "msg": "Success",
                            "data": {
                                "id": 12,
                                "nodes": [
                                    {
                                        "id": 2,
                                        "nodeUid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                        "name": "测试节点 修改名称",
                                        "status": False
                                    }
                                ],
                                "founderUser": {
                                    "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                    "username": "超级管理员"
                                },
                                "spider": {
                                    "id": 1,
                                    "spiderUid": "ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                                    "name": "测试爬虫0",
                                    "status": False
                                },
                                "createTime": "2024-08-24 16:11:56",
                                "updateTime": "2024-08-24 16:11:56",
                                "taskUid": "d3702283-16c7-472c-82f4-f66ba38e99df",
                                "name": "测试任务1",
                                "status": False,
                                "isTiming": False,
                                "cronExpression": ""
                            }
                        }
                    }
                })
        }
    )
    def update(self, request, *args, **kwargs):
        if 'founder' in request.data:
            del request.data['founder']
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='任务删除',
        operation_description='删除任务',
        tags=['任务管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success"
                    }
                })
        }
    )
    def destroy(self, request, *args, **kwargs):
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
