from apps.Node.models import NodeModel
from django_redis import get_redis_connection
from task_celery.main import app as celery_app


@celery_app.task
def node_detection():
    """
    定时检测服务节点是否存活，存在数据库中状态为存活的当不存活时走webhook通知
    """
    # nodes = [i.node_uid for i in NodeModel.objects.all() if i.node_uid]
    conn = get_redis_connection('node_detection')
    search_nodes = []
    for key in conn.scan_iter():
        key: bytes
        node_key = key.decode('utf-8')
        search_nodes.append(node_key)
    return search_nodes
