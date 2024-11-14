import asyncio
import logging

from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from utils.node_api import NodeApi
from utils.node_stat import get_node_conn

logger = logging.getLogger(__name__)


class LogsConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        super().__init__()
        self.conn = None
        self.task_uid = None
        self.node_uid = None
        self.subscribe_key = None
        self.stop_event = asyncio.Event()
        self.task = None

    async def websocket_connect(self, message):
        """
        连接
        """
        self.conn = get_node_conn()
        self.task_uid = self.scope['url_route']['kwargs']['task_uid']
        self.node_uid = self.scope['url_route']['kwargs']['node_uid']
        NodeApi.node_task_start_log(self.conn, self.node_uid, self.task_uid)
        await self.accept()
        self.subscribe_key = "{}{}".format(self.node_uid, self.task_uid)
        self.task = asyncio.create_task(self.read_logs())
        logger.info("websocket connect {}".format(self.scope['url_route']))

    async def websocket_receive(self, message):
        """
        接收消息
        """
        logger.info("websocket receive {}".format(message))

    async def websocket_disconnect(self, message):
        """
        断开连接
        """
        self.stop_event.set()
        await self.task
        NodeApi.node_task_stop_log(self.conn, self.node_uid, self.task_uid)
        self.conn.close()
        logger.info("websocket disconnect {}".format(message))
        raise StopConsumer()

    async def read_logs(self):
        pubsub = self.conn.pubsub()
        pubsub.subscribe(self.subscribe_key)
        try:
            while not self.stop_event.is_set():
                message = pubsub.get_message(timeout=1)
                if message and message['type'] == 'message':
                    data = message['data'].decode('utf-8')
                    await self.send(text_data=data)
                await asyncio.sleep(0.6)
        finally:
            pubsub.unsubscribe(self.subscribe_key)
