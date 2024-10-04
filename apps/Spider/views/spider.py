"""
记录爬虫的基本信息
"""
from uuid import uuid4

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers
from rest_framework.views import Request

from apps.Spider.models import SpiderModel
from apps.Spider.serializer import SpiderSerializer, SpiderOptionSerializer
from utils.viewset import CustomModelViewSet, CustomGenericViewSet, CustomListMixin
from django.conf import settings


class SpiderViewSet(CustomModelViewSet):
    queryset = SpiderModel.objects.all()
    serializer_class = SpiderSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary='爬虫列表',
        operation_description='爬虫列表',
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
                description='爬虫名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'founder',
                openapi.IN_QUERY,
                description='创建人搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'spiderUid',
                openapi.IN_QUERY,
                description='爬虫ID搜索',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description='状态搜索(true|false)',
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        tags=['爬虫管理'],
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
                                    "id": 1,
                                    "founderUser": {
                                        "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                        "username": "超级管理员"
                                    },
                                    "createTime": "2024-08-24 15:44:53",
                                    "updateTime": "2024-08-24 15:44:53",
                                    "name": "测试爬虫",
                                    "spiderUid": "ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                                    "resources": "/data/spider_project/ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                                    "status": False
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
        operation_summary='爬虫详情',
        operation_description='爬虫详情',
        tags=['爬虫管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "id": 2,
                            "founderUser": {
                                "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                "username": "超级管理员"
                            },
                            "createTime": "2024-08-24 15:48:18",
                            "updateTime": "2024-08-24 15:48:18",
                            "name": "测试爬虫1",
                            "spiderUid": "ddae795f-f6e7-444d-8f34-600f16b529f4",
                            "resources": "/data/spider_project/ddae795f-f6e7-444d-8f34-600f16b529f4",
                            "status": False
                        }
                    }
                })
        }
    )
    def retrieve(self, request: Request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='创建爬虫',
        operation_description='创建爬虫',
        manual_parameters=[],
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['name'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='爬虫名'),
            }
        ),
        tags=['爬虫管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": {
                            "id": 2,
                            "founderUser": {
                                "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                "username": "超级管理员"
                            },
                            "createTime": "2024-08-24 15:48:18",
                            "updateTime": "2024-08-24 15:48:18",
                            "name": "测试爬虫1",
                            "spiderUid": "ddae795f-f6e7-444d-8f34-600f16b529f4",
                            "resources": "/data/spider_project/ddae795f-f6e7-444d-8f34-600f16b529f4",
                            "status": False
                        }
                    }
                })
        }
    )
    def create(self, request, *args, **kwargs):
        request.data['founder'] = 1
        spider_uid = uuid4()
        request.data['spiderUid'] = spider_uid
        # TODO: 为爬虫创建项目文件夹
        resources = settings.IDE_RESOURCES / str(spider_uid)
        resources.mkdir(parents=True)
        request.data['resources'] = str(resources)
        # request.data['founder'] = request.user.uid
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='爬虫修改',
        operation_description='爬虫更新',
        tags=['爬虫管理'],
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
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='爬虫名'),
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
                            "id": 1,
                            "founderUser": {
                                "uid": "109cd841-5dfa-4f69-aa6c-2d7e9f73c383",
                                "username": "超级管理员"
                            },
                            "createTime": "2024-08-24 15:44:53",
                            "updateTime": "2024-08-24 15:52:28",
                            "name": "测试爬虫0",
                            "spiderUid": "ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                            "resources": "/data/spider_project/ea34b00d-9e51-40f1-8b6c-b64eec81ab85",
                            "status": True
                        }
                    }
                })
        }
    )
    def update(self, request, *args, **kwargs):
        if 'founder' in request.data:
            del request.data['founder']
        if 'spiderUid' in request.data:
            del request.data['spiderUid']
        if 'resources' in request.data:
            del request.data['resources']
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='爬虫删除',
        operation_description='删除爬虫',
        tags=['爬虫管理'],
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

    @swagger_auto_schema(
        operation_summary='爬虫选项列表',
        operation_description='爬虫选项列表',
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='爬虫名称模糊搜索',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['爬虫管理'],
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
                                    "id": 1,
                                    "name": "测试爬虫",
                                }
                            ]
                        }
                    }
                })
        }
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        filter_data = queryset
        name = self.request.query_params.get('name', None)
        if name: filter_data = filter_data.filter(name__icontains=name)
        return filter_data


router = routers.DefaultRouter()
router.register('spider', SpiderViewSet, basename='spider')
router.register('spiderOption', SpiderOptionViewSet, basename='spider-option')
