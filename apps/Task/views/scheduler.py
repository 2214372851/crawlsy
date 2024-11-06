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
import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.Task.models import TaskModel
from utils.code import Code
from utils.node_stat import get_node_conn
from utils.response import CustomResponse
from utils.status import Status


class SchedulerView(APIView):

    @swagger_auto_schema(
        operation_summary='任务状态',
        operation_description='获取任务运行状态信息',
        manual_parameters=[
            openapi.Parameter('nodeUid', openapi.IN_QUERY, description='节点唯一标识', type=openapi.TYPE_STRING),
            openapi.Parameter('taskId', openapi.IN_QUERY, description='任务唯一标识', type=openapi.TYPE_STRING),
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
        task_id = request.query_params.get('taskId')

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
        if task_id not in running_taks:
            return CustomResponse(
                code=Code.OK,
                msg='success',
                data={
                    'status': Status.NOT_EXIST
                }
            )
        response = requests.get(
            'http:{}:{}/scheduler/node/{}/'.format(
                service.get('host'),
                service.get('port'),
                task_id
            ),
            params={
                'token': node_uid
            }
        )

        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data={
                'status': response.status_code
            }
        )

    @swagger_auto_schema(
        operation_summary='任务终止',
        operation_description='任务终止',
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description='任务唯一标识', type=openapi.TYPE_STRING),
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
        task_id = request.query_params.get('id')

        task = TaskModel.objects.get(pk=task_id)
        nodes = task.taskNodes.all()
        if not nodes:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='当前任务未部署',
            )
        conn = get_node_conn()
        errors = {}
        for node in nodes:
            try:
                service = conn.get(f"{node.nodeUid}_stat")
                service = json.loads(service.decode('utf-8'))
                response = requests.delete(
                    'http:{}:{}/scheduler/node/{}/'.format(
                        service.get('host'),
                        service.get('port'),
                        task_id
                    ),
                    params={
                        'token': service.get('token')
                    }
                )
                response.raise_for_status()
            except Exception as e:
                errors[node.nodeUid] = str(e)
        if errors:
            return CustomResponse(
                code=Code.FAILED_PRECONDITION,
                msg='任务终止失败',
                data=errors
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    def put(self, request: Request):
        """
        重新部署任务
        """
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    def post(self, request: Request):
        """
        部署任务
        """
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )
