import redis
from django.conf import settings

redis_pool = redis.ConnectionPool.from_url(settings.NODE_SERVICE_URL)


def get_node_conn():
    return redis.Redis(connection_pool=redis_pool)