import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.Node.models import NodeModel
from utils.code import Code
from utils.node_stat import get_node_conn
from utils.response import CustomResponse


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
        exclude_nodes = {node.nodeUid for node in NodeModel.objects.all()}
        conn = get_node_conn()
        search_nodes = []
        for key in conn.keys('*_stat'):
            key: bytes
            node_key = key.decode('utf-8')
            if node_key not in exclude_nodes:
                node_info = json.loads(conn.get(node_key).decode('utf-8'))
                del node_info['token']
                del node_info['node_ip']
                del node_info['node_port']
                search_nodes.append(node_info)
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data={
                'total': len(search_nodes),
                'list': search_nodes
            }
        )
