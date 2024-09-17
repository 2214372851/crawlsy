from django_redis import get_redis_connection
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from utils.code import Code
from utils.response import CustomResponse
from apps.Node.models import NodeModel


class SearchNodeView(APIView):
    """
    节点发现视图
    """

    @swagger_auto_schema(
        operation_summary='搜索节点',
        operation_description='自动发现服务中的节点',
        tags=['节点管理'],
        responses={
            200: openapi.Response(
                description='ok',
                examples={
                    'application/json': {
                        "code": 0,
                        "msg": "Success",
                        "data": [
                            "787237b3-f59e-4aa3-9eba-7d98f122b6d5"
                        ]
                    }
                })
        }
    )
    def get(self, request: Request):
        # TODO: 等待子节点模块完成
        exclude_nodes = {node.nodeUid for node in NodeModel.objects.all()}
        conn = get_redis_connection('node_detection')
        search_nodes = []
        for key in conn.scan_iter():
            key: bytes
            node_key = key.decode('utf-8')
            if node_key not in exclude_nodes:
                search_nodes.append(node_key)
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data=search_nodes
        )
