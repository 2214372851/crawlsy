import json
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


    def get(self, request: Request):
        exclude_nodes = {node.nodeUid for node in NodeModel.objects.all()}
        conn = get_node_conn()
        search_nodes = []
        for key in conn.keys('stat:*'):
            key: bytes
            node_key = key.decode('utf-8')
            if node_key not in exclude_nodes:
                node_info = json.loads(conn.get(node_key).decode('utf-8'))
                del node_info['node_host']
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
