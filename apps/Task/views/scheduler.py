"""
任务调度器
    调度任务
        负载均衡器
        任务运行
        任务结束
        任务暂停
    任务监控
"""
import json
import logging
from concurrent.futures import ThreadPoolExecutor

from rest_framework.request import Request
from rest_framework.views import APIView

from apps.Node.models import NodeModel
from apps.Task.models import TaskModel
from utils.code import Code
from utils.node_api import NodeApi
from utils.node_stat import get_node_conn
from utils.response import CustomResponse
from utils.status import Status

logger = logging.getLogger('django')


class SchedulerView(APIView):

    def get(self, request: Request):
        """
        获取任务运行状态信息
        :param request:
        :return:
        """
        node_uid = request.query_params.get('nodeUid')
        task_uid = request.query_params.get('taskUid')

        conn = get_node_conn()
        service = conn.get(f"stat:{node_uid}")
        if service is None:
            return CustomResponse(
                code=Code.OK,
                msg='success',
                data={
                    'status': Status.OFFLINE
                }
            )
        service = json.loads(service.decode('utf-8'))
        running_taks = {i['task_id'] for i in service['tasks']}
        if task_uid not in running_taks:
            return CustomResponse(
                code=Code.OK,
                msg='success',
                data={
                    'status': Status.NOT_EXIST
                }
            )
        try:
            status, message, result = NodeApi().node_task_stat(service, task_uid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return CustomResponse(
                code=Code.UNKNOWN,
                msg=str(e),
            )
        if not status:
            return CustomResponse(
                code=Code.UNKNOWN,
                msg=message,
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data={
                'status': result
            }
        )

    def delete(self, request: Request):
        """
        停止所有节点上的该任务
        """
        task_uid = request.query_params.get('taskUid')

        task = TaskModel.objects.filter(taskUid=task_uid).first()
        if not task:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='任务不存在',
            )
        nodes = task.taskNodes.all()
        if not nodes:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='当前任务无任务节点',
            )
        conn = get_node_conn()
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for node in nodes:
                futures[node.nodeUid] = executor.submit(NodeApi().node_task_stop, conn, node.nodeUid, task_uid)
            results = [i.result() for i in futures.values() if i.result()]
        for status, message, result in results:
            if not status:
                return CustomResponse(
                    code=Code.UNKNOWN,
                    msg=message,
                )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    def post(self, request: Request):
        """
        部署任务
            多次部署已经存在的任务的节点将不做处理，未部署的节点将完成部署流程
        """
        task_uid = request.data.get('taskUid')
        task: TaskModel = TaskModel.objects.filter(taskUid=task_uid).first()
        if not task:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='任务不存在',
            )
        if task.isTiming:
            # TODO: 定时任务特殊处理
            pass
        nodes = task.taskNodes.all()
        if not nodes:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='当前任务无任务节点',
            )
        conn = get_node_conn()
        command = task.taskSpider.command
        if not command:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='爬虫未配置启动命令',
            )
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for node in nodes:
                futures[node.nodeUid] = executor.submit(
                    NodeApi().node_task_start, conn,
                    node.nodeUid, task_uid, command
                )
            results = [i.result() for i in futures.values() if i.result()]
            for status, message, result in results:
                if not status:
                    return CustomResponse(
                        code=Code.UNKNOWN,
                        msg=message,
                    )
            return CustomResponse(
                code=Code.OK,
                msg='Success',
            )

    def put(self, request: Request):
        """
        重新部署任务
        """
        task_uid = request.query_params.get('taskUid')
        task = TaskModel.objects.filter(taskUid=task_uid).first()
        if not task:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='任务不存在',
            )
        if task.isTiming:
            # TODO: 定时任务特殊处理
            pass
        nodes = task.taskNodes.all()
        if not nodes:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='当前任务无任务节点',
            )
        conn = get_node_conn()
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for node in nodes:
                futures[node.nodeUid] = executor.submit(NodeApi().node_task_reload, conn, node.nodeUid, task_uid)
            results = [i.result() for i in futures.values() if i.result()]
            for status, message, result in results:
                if not status:
                    return CustomResponse(
                        code=Code.UNKNOWN,
                        msg=message,
                    )
            return CustomResponse(
                code=Code.OK,
                msg='Success',
            )


class SchedulerPackageView(APIView):
    """
    调度包管理
    """

    def get(self, request: Request):
        conn = get_node_conn()
        nodes = NodeModel.objects.filter(status=True)
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for node in nodes:
                futures[node.nodeUid] = executor.submit(NodeApi().node_pip_list, conn, node.nodeUid)
            results = [i.result() for i in futures.values() if not i.exception()]
        response_data = {}
        for status, message, result in results:
            if not status:
                return CustomResponse(
                    code=Code.UNKNOWN,
                    msg=message,
                )
            for item in result:
                key = '{}:{}'.format(item['name'], item['version'])
                response_data[key] = {
                    'name': item['name'],
                    'version': item['version']
                }
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data={
                'total': len(response_data),
                'list': response_data.values()
            }
        )

    def post(self, request: Request):
        package_name = request.data.get('packageName', '').strip()
        if not package_name:
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg='调度包名称不能为空',
            )
        conn = get_node_conn()
        nodes = NodeModel.objects.filter(status=True)
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for node in nodes:
                futures[node.nodeUid] = executor.submit(NodeApi().node_pip_install, conn, node.nodeUid, package_name)
            results = [i.result() for i in futures.values() if i.result()]
        for status, message, result in results:
            if not status:
                return CustomResponse(
                    code=Code.UNKNOWN,
                    msg=message,
                )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    def delete(self, request: Request):
        package_name = request.query_params.get('packageName', '').strip()
        if not package_name:
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg='调度包名称不能为空',
            )
        conn = get_node_conn()
        nodes = NodeModel.objects.filter(status=True)
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for node in nodes:
                futures[node.nodeUid] = executor.submit(NodeApi().node_pip_uninstall, conn, node.nodeUid, package_name)
            results = [i.result() for i in futures.values() if i.result()]
            for status, message, result in results:
                if not status:
                    return CustomResponse(
                        code=Code.UNKNOWN,
                        msg=message,
                    )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    def put(self, request: Request):
        package_name = request.query_params.get('packageName', '').strip()
        if not package_name:
            return CustomResponse(
                code=Code.INVALID_ARGUMENT,
                msg='调度包名称不能为空',
            )
        conn = get_node_conn()
        nodes = NodeModel.objects.filter(status=True)
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {}
            for node in nodes:
                futures[node.nodeUid] = executor.submit(NodeApi().node_pip_update, conn, node.nodeUid, package_name)
            results = [i.result() for i in futures.values() if i.result()]
        for status, message, result in results:
            if not status:
                return CustomResponse(
                    code=Code.UNKNOWN,
                    msg=message,
                )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )
