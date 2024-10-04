from pathlib import Path

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.Spider.models import SpiderModel
from utils.code import Code
from utils.file import is_text_file
from utils.response import CustomResponse


class IdeApiView(APIView):
    """
    IDE视图
    """

    @swagger_auto_schema(
        operation_summary='资源列表',
        operation_description='资源列表',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_QUERY,
                description='资源ID',
                type=openapi.TYPE_NUMBER
            ),
        ],
        tags=['编辑器管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {}
                })
        }
    )
    def get(self, request: Request):
        resource_id = request.query_params.get('id')
        if not resource_id: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数错误"
        )
        resource = SpiderModel.objects.get(pk=resource_id)
        if not resource: return CustomResponse(
            code=Code.NOT_FOUND,
            msg="资源不存在"
        )
        resource_path = Path(resource.resources)
        if not resource_path.exists():
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源不存在")
        flag_path = resource_path.parent

        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data=[
                {
                    "isFile": i.is_file(),
                    "path": str(i.relative_to(flag_path)),
                    "name": i.name
                } for i in resource_path.iterdir()
            ]
        )

    @swagger_auto_schema(
        operation_summary='资源重命名',
        operation_description='资源重命名',
        tags=['编辑器管理'],
        manual_parameters=[
            openapi.Parameter(
                'path',
                openapi.IN_QUERY,
                description='文件路径',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description='文件名称',
                type=openapi.TYPE_STRING
            )
        ]
    )
    def put(self, request: Request):
        path = request.query_params.get('path')
        name = request.query_params.get('name')
        resource_path = settings.IDE_RESOURCES / path
        if not path or not name: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数错误"
        )
        if not resource_path.exists():
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源不存在")
        resource_path.rename(resource_path.parent / name)
        return CustomResponse(
            code=Code.OK,
            msg="Success"
        )

    @swagger_auto_schema(
        operation_summary='新建资源',
        operation_description='新建资源',
        tags=['编辑器管理'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'path': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    )
    def post(self, request: Request):
        path = request.data.get('path')
        name = request.data.get('name')
        resource_path = settings.IDE_RESOURCES / path
        if not path or not name: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数错误"
        )
        if resource_path.exists():
            return CustomResponse(code=Code.ALREADY_EXISTS, msg="资源已存在")
        if name.endswith('/'):
            resource_path.mkdir(parents=True, exist_ok=True)
        else:
            resource_path.parent.mkdir(parents=True, exist_ok=True)
            resource_path.touch()

        return CustomResponse(
            code=Code.OK,
            msg="Success"
        )

    @swagger_auto_schema(
        operation_summary='删除资源',
        operation_description='删除资源',
        tags=['编辑器管理'],
        manual_parameters=[
            openapi.Parameter(
                'path',
                openapi.IN_QUERY,
                description='参考项key',
                type=openapi.TYPE_STRING
            )
        ]
    )
    def delete(self, request: Request):
        path = request.query_params.get('path')
        resource_path = settings.IDE_RESOURCES / path
        if not path: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数错误"
        )
        if not resource_path.exists():
            return CustomResponse(code=Code.NOT_FOUND, msg="资源不存在")
        resource_path.unlink()
        return CustomResponse(
            code=Code.OK,
            msg="Success"
        )


class IdeLazyView(APIView):
    """
    IDE懒加载视图
    """

    @swagger_auto_schema(
        operation_summary='懒加载',
        operation_description='懒加载',
        manual_parameters=[
            openapi.Parameter(
                'path',
                openapi.IN_QUERY,
                description='参考项key',
                type=openapi.TYPE_STRING
            )
        ],
        tags=['编辑器管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {}
                }
            )
        }
    )
    def get(self, request: Request):
        path = request.query_params.get('path')
        if not path: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数错误"
        )
        resource_path = settings.IDE_RESOURCES / path
        if not resource_path.exists():
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源不存在")
        if resource_path.is_file(): return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="文件无子项"
        )
        flag_path = resource_path.relative_to(settings.IDE_RESOURCES)

        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data=[
                {
                    "isFile": i.is_file(),
                    "path": str(resource_path / i.name),
                    "name": i.name
                } for i in resource_path.iterdir()
            ]
        )


class IdeFileView(APIView):
    """
    IDE文件视图
    """

    @swagger_auto_schema(
        operation_summary='文件内容',
        operation_description='文件内容',
        manual_parameters=[
            openapi.Parameter(
                'path',
                openapi.IN_QUERY,
                description='文件路径',
                type=openapi.TYPE_STRING
            ),
        ],
        tags=['编辑器管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {}
                }
            )
        }
    )
    def post(self, request: Request):
        path = request.data.get('path')
        print(path)
        resource_path = settings.IDE_RESOURCES / path
        print(resource_path)
        if not path or not resource_path.exists():
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg="参数错误"
            )
        if resource_path.is_dir():
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg="目录无法操作"
            )
        if not is_text_file(resource_path):
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg="文件类型不支持"
            )
        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data=resource_path.read_text(encoding='utf-8')
        )
