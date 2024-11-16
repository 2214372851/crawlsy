import redis
from celery import shared_task
from django.conf import settings

from apps.Node.models import NodeModel
import logging


logger = logging.getLogger('django')


@shared_task
def node_detection():
    """
    定时检测服务节点是否存活，存在数据库中状态为存活的当不存活时走webhook通知
    """
    conn = redis.StrictRedis.from_url(settings.NODE_SERVICE_URL)

    search_nodes = []
    for key in conn.keys('stat:*'):
        key: bytes
        node_key = key.decode('utf-8')
        search_nodes.append(node_key.replace('stat:', ''))
    for node in NodeModel.objects.all():

        status = str(node.nodeUid) in search_nodes
        if node.status != status:
            logger.info(f'节点{node.name}状态改变为{status}')
            node.status = status
            node.save()
