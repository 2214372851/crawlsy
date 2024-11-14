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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.Task.models import TaskModel
from utils.code import Code
from utils.node_api import NodeApi
from utils.node_stat import get_node_conn
from utils.response import CustomResponse
from utils.status import Status

logger = logging.getLogger(__name__)


class SchedulerView(APIView):

    @swagger_auto_schema(
        operation_summary='任务状态',
        operation_description='获取任务运行状态信息',
        manual_parameters=[
            openapi.Parameter('nodeUid', openapi.IN_QUERY, description='节点唯一标识', type=openapi.TYPE_STRING),
            openapi.Parameter('taskUid', openapi.IN_QUERY, description='任务唯一标识', type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description='Success',
                examples={}
            )
        }
    )
    def get(self, request: Request):
        """
        获取任务运行状态信息
        :param request:
        :return:
        """
        node_uid = request.query_params.get('nodeUid')
        task_uid = request.query_params.get('taskUid')

        conn = get_node_conn()
        service = conn.get(f"{node_uid}_stat")
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
            response = NodeApi.node_task_stat(service, node_uid, task_uid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return CustomResponse(
                code=Code.UNKNOWN,
                msg=str(e),
            )
        response_data = response.json()
        if response_data.get('code') != Code.OK:
            return CustomResponse(
                code=response_data.get('code'),
                msg=response.json().get('msg'),
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data={
                'status': response.json().get('status')
            }
        )

    @swagger_auto_schema(
        operation_summary='任务终止',
        operation_description='任务终止',
        manual_parameters=[
            openapi.Parameter('taskUid', openapi.IN_QUERY, description='任务唯一标识', type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description='Success',
                examples={}
            )
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
                futures[node.nodeUid] = executor.submit(NodeApi.node_task_stop, conn, node.nodeUid, task_uid)
            errors = [
                {
                    'nodeUid': str(uid),
                    'error': str(future.exception())
                } for uid, future in futures.items() if future.exception()
            ]
        if errors:
            logger.error(errors[0]['error'], exc_info=True)
            return CustomResponse(
                code=Code.FAILED_PRECONDITION,
                msg='任务终止失败',
                data=errors
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    @swagger_auto_schema(
        operation_summary='任务部署',
        operation_description='部署任务',
        request_body=openapi.Schema(
            # 构造的请求体为 dict 类型
            type=openapi.TYPE_OBJECT,
            # 构造的请求体中 必填参数 列表
            required=['name'],
            # 自定义请求体 ， key为请求参数名称，值为参数描述
            properties={
                'taskUid': openapi.Schema(type=openapi.TYPE_STRING, description='任务唯一识别ID'),
            }
        ),
        responses={
            200: openapi.Response(
                description='Success',
                examples={}
            )
        }
    )
    def post(self, request: Request):
        """
        部署任务
            多次部署已经存在的任务的节点将不做处理，未部署的节点将完成部署流程
        """
        task_uid = request.data.get('taskUid')
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
                futures[node.nodeUid] = executor.submit(NodeApi.node_task_start, conn, node.nodeUid, task_uid)
            errors = [
                {
                    'nodeUid': str(uid),
                    'error': str(future.exception())
                } for uid, future in futures.items() if future.exception() is not None
            ]
        if errors:
            logger.error(errors[0]['error'], exc_info=True)
            return CustomResponse(
                code=Code.FAILED_PRECONDITION,
                msg='任务部署失败',
                data=errors
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    @swagger_auto_schema(
        operation_summary='任务重新部署',
        operation_description='重新部署任务',
        manual_parameters=[
            openapi.Parameter('taskUid', openapi.IN_QUERY, description='任务唯一标识', type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description='Success',
                examples={}
            )
        }
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
                futures[node.nodeUid] = executor.submit(NodeApi.node_task_reload, conn, node.nodeUid, task_uid)
            errors = [
                {
                    'nodeUid': str(uid),
                    'error': str(future.exception())
                } for uid, future in futures.items() if future.exception()
            ]
        if errors:
            logger.error(errors[0]['error'], exc_info=True)
            return CustomResponse(
                code=Code.FAILED_PRECONDITION,
                msg='任务重载失败',
                data=errors
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )


class SchedulerLogView(APIView):
    """
    调度日志
    """

    @swagger_auto_schema(
        operation_summary='开启任务日志',
        operation_description='开启任务日志',
        manual_parameters=[
            openapi.Parameter('nodeUid', openapi.IN_QUERY, description='节点唯一标识', type=openapi.TYPE_STRING),
            openapi.Parameter('taskUid', openapi.IN_QUERY, description='任务唯一标识', type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description='Success',
            )
        }
    )
    def get(self, request: Request):
        node_uid = request.query_params.get('nodeUid')
        task_uid = request.query_params.get('taskUId')
        conn = get_node_conn()

        try:
            response = NodeApi.node_task_start_log(conn, node_uid, task_uid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return CustomResponse(
                code=Code.ABORTED,
                msg=str(e),
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data=response.json().get('data')
        )

    @swagger_auto_schema(
        operation_summary='关闭任务日志',
        operation_description='关闭任务日志',
        manual_parameters=[
            openapi.Parameter('nodeUid', openapi.IN_QUERY, description='节点唯一标识', type=openapi.TYPE_STRING),
            openapi.Parameter('taskUid', openapi.IN_QUERY, description='任务唯一标识', type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response(
                description='Success',
            )
        }
    )
    def delete(self, request: Request):
        node_uid = request.query_params.get('nodeUid')
        task_uid = request.query_params.get('taskUId')
        conn = get_node_conn()

        try:
            response = NodeApi.node_task_stop_log(conn, node_uid, task_uid)
        except Exception as e:
            logger.error(e, exc_info=True)
            return CustomResponse(
                code=Code.ABORTED,
                msg=str(e),
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data=response.json().get('data')
        )
