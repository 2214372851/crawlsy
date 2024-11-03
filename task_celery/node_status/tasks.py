from apps.Node.models import NodeModel
from django.conf import settings
import redis
from celery import shared_task
from task_celery.main import app as celery_app


@shared_task
def node_detection():
    """
    定时检测服务节点是否存活，存在数据库中状态为存活的当不存活时走webhook通知
    """
    nodes = [i.nodeUid for i in NodeModel.objects.all() if i.status]
    conn = redis.StrictRedis.from_url(settings.NODE_SERVICE_URL)

    search_nodes = nodes
    for key in conn.scan_iter():
        key: bytes
        node_key = key.decode('utf-8')
        search_nodes.append(node_key)
    print(search_nodes)
    return search_nodes
