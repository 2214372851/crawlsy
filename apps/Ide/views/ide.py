import shutil
from pathlib import Path

from django.conf import settings

from rest_framework.request import Request
from rest_framework.views import APIView

from apps.Spider.models import SpiderModel
from utils.code import Code
from utils.file import is_text_file, is_valid_filename
from utils.response import CustomResponse


class IdeApiView(APIView):
    """
    IDE视图
    """

    def get(self, request: Request):
        resource_id = request.query_params.get('id')
        if not resource_id: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数为空"
        )
        resource = SpiderModel.objects.filter(pk=resource_id).first()
        if not resource: return CustomResponse(
            code=Code.NOT_FOUND,
            msg="资源不存在"
        )
        resource_path = Path(resource.resources)
        if not resource_path.exists():
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源不存在")
        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data=[
                {
                    "key": str(resource_path.relative_to(settings.IDE_RESOURCES)),
                    "isLeaf": False,
                    "title": resource.name
                }
            ]
        )

    def put(self, request: Request):
        path = request.query_params.get('path')
        name = request.query_params.get('name')
        resource_path = settings.IDE_RESOURCES / path
        if not path or not name: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数为空"
        )
        if '/' in name:
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="文件名不能包含路径")
        if not resource_path.exists():
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源不存在")
        new_path = resource_path.parent / name
        if new_path.exists():
            return CustomResponse(code=Code.ALREADY_EXISTS, msg="资源已存在不能重复命名")
        if not is_valid_filename(name):
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源名不合法")
        resource_path.rename(resource_path.parent / name)
        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data={
                "key": str(new_path.relative_to(settings.IDE_RESOURCES)),
                "isLeaf": new_path.is_file(),
                "title": new_path.name
            }
        )

    def post(self, request: Request):
        path = request.data.get('path')
        name = request.data.get('name')
        resource_path = settings.IDE_RESOURCES / path / name
        if not path or not name: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数为空"
        )
        if '..' in name or len(Path(name).parts) > 1 or name.startswith('/'):
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="不能操作跨级资源")
        if resource_path.exists():
            return CustomResponse(code=Code.ALREADY_EXISTS, msg="资源已存在")
        if not is_valid_filename(resource_path.name):
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源名不合法")
        if name.endswith('/'):
            resource_path.mkdir(exist_ok=True)
        else:
            resource_path.touch()
        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data={
                "key": str(resource_path.relative_to(settings.IDE_RESOURCES)),
                "isLeaf": resource_path.is_file(),
                "title": resource_path.name
            }
        )

    def delete(self, request: Request):
        path = request.query_params.get('path')
        if not path: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数为空"
        )
        resource_path = settings.IDE_RESOURCES / path
        if resource_path.parent.name == settings.IDE_RESOURCES.name:
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="不能删除根目录")
        if not resource_path.exists():
            return CustomResponse(code=Code.NOT_FOUND, msg="资源不存在")
        if resource_path.is_dir():
            shutil.rmtree(resource_path)
        else:
            resource_path.unlink()
        return CustomResponse(
            code=Code.OK,
            msg="Success"
        )


class IdeLazyView(APIView):
    """
    IDE懒加载视图
    """

    def get(self, request: Request):
        path = request.query_params.get('path')
        if not path: return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="参数为空"
        )
        resource_path = settings.IDE_RESOURCES / path
        if not resource_path.exists():
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="资源不存在")
        if resource_path.is_file(): return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg="文件无子项"
        )
        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data=[
                {
                    "isLeaf": i.is_file(),
                    "key": str(resource_path.joinpath(i.name).relative_to(settings.IDE_RESOURCES)),
                    "title": i.name
                } for i in resource_path.iterdir()
            ]
        )


class IdeFileView(APIView):
    """
    IDE文件视图
    """

    def get(self, request: Request):
        path = request.query_params.get('path')
        resource_path = settings.IDE_RESOURCES / path
        if not path or not resource_path.exists():
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg="参数为空或资源不存在"
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
        if resource_path.stat().st_size > settings.IDE_MAX_FILE_SIZE:
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg="文件过大"
            )
        return CustomResponse(
            code=Code.OK,
            msg="Success",
            data=resource_path.read_text(encoding='utf-8')
        )

    def put(self, request: Request):
        path = request.data.get('path')
        content = request.data.get('content')
        resource_path = settings.IDE_RESOURCES / path
        if not path or not content or not resource_path.exists():
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg="参数为空或资源不存在"
            )
        if not is_text_file(resource_path):
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg="文件类型不支持"
            )
        resource_path.write_text(content.replace('\r\n', '\n'), encoding='utf-8')
        return CustomResponse(
            code=Code.OK,
            msg="Success"
        )

    def post(self, request: Request):
        path = request.data.get('path')
        file = request.FILES.get('file')
        if not path or not file:
            return CustomResponse(
                status=400,
                code=Code.INVALID_ARGUMENT,
                msg="参数为空或文件不存在"
            )
        resource_path = settings.IDE_RESOURCES / path / file.name
        if resource_path.exists():
            return CustomResponse(code=Code.ALREADY_EXISTS, msg="文件已存在")
        if not is_valid_filename(resource_path.name):
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="文件名不合法")
        if file.size > settings.IDE_MAX_FILE_SIZE:
            return CustomResponse(code=Code.INVALID_ARGUMENT, msg="文件过大")
        with resource_path.open('wb') as f:
            while True:
                chunk = file.read(1024)
                print(chunk, '---------------')
                if not chunk: break
                f.write(chunk)
        return CustomResponse(
            code=Code.OK,
            msg="Success"
        )
