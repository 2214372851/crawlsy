import json

from rest_framework.views import Request
from apps.Node.models import NodeModel
from rest_framework import routers

from utils.node_stat import get_node_conn
from utils.viewset import CustomGenericViewSet, CustomListMixin
from utils.code import Code
from utils.response import CustomResponse


class MonitorViewSet(CustomGenericViewSet, CustomListMixin):

    def list(self, request: Request, *args, **kwargs):
        nodes = NodeModel.objects.all()
        monitor_data = []
        for node in nodes:
            data = get_node_conn().lrange(f'monitor:{node.nodeUid}', 0, 3000)[::40]
            monitor_data.append({
                'nodeUid': node.nodeUid,
                'monitor': [json.loads(item.decode('utf-8')) for item in data][::-1]
            })
        return CustomResponse(code=Code.OK, msg='Success', data=monitor_data)


router = routers.DefaultRouter()
router.register(r'monitor', MonitorViewSet, basename='monitor')
