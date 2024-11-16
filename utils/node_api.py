import json
import pickle

import grpc

from utils.exception import SchedulerException
from utils.proto import manager_pb2_grpc as pb2c, manager_pb2 as pb2


class NodeApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NodeApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def _load(data):
        return pickle.loads(data)

    @staticmethod
    def _get_service(conn, node_uid):
        service = conn.get(f"stat:{node_uid}")
        if not service: raise SchedulerException('节点离线')
        return json.loads(service.decode('utf-8'))

    def node_task_stat(self, service, task_uid):
        channel = grpc.insecure_channel(
            '{}:{}'.format(
                service.get('node_host'),
                service.get('node_port')
            )
        )
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.TaskStatus(pb2.TaskStatusRequest(task_uid=task_uid))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_task_stop(self, conn, node_uid, task_uid):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.TaskDelete(pb2.TaskDeleteRequest(task_uid=task_uid))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_task_start(self, conn, node_uid, task_uid, command):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.TaskStart(pb2.TaskStartRequest(task_uid=task_uid, command=command))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_task_reload(self, conn, node_uid, task_uid):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.TaskReload(pb2.TaskReloadRequest(task_uid=task_uid))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_task_start_log(self, conn, node_uid, task_uid):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.TaskLogsOpen(pb2.TaskLogsOpenRequest(task_uid=str(task_uid)))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_task_stop_log(self, conn, node_uid, task_uid):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.TaskLogsClose(pb2.TaskLogsCloseRequest(task_uid=str(task_uid)))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_pip_list(self, conn, node_uid):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.PipList(pb2.PipRequest())
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_pip_install(self, conn, node_uid, package_name):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.PipInstall(pb2.PipRequest(package_name=package_name))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_pip_uninstall(self, conn, node_uid, package_name):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.PipUninstall(pb2.PipRequest(package_name=package_name))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result

    def node_pip_update(self, conn, node_uid, package_name):
        service = self._get_service(conn, node_uid)
        channel = grpc.insecure_channel('{}:{}'.format(service.get('node_host'), service.get('node_port')))
        client = pb2c.SpiderNodeServiceStub(channel)
        result = client.PipUpdate(pb2.PipRequest(package_name=package_name))
        status = result.status
        message = result.message
        result = self._load(result.result)
        return status, message, result
