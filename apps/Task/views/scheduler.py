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
        response = requests.get(
            'http:{}:{}/scheduler/node/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid
            ),
            params={
                'token': node_uid
            }
        )
        if response.json().get('code') != Code.OK:
            return CustomResponse(
                code=response.json().get('code'),
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
        task_uid = request.query_params.get('taskUid')

        task = TaskModel.objects.get(taskUid=task_uid)
        nodes = task.taskNodes.all()
        if not nodes:
            return CustomResponse(
                code=Code.NOT_FOUND,
                msg='当前任务无任务节点',
            )
        conn = get_node_conn()
        errors = {}
        for node in nodes:
            try:
                service = conn.get(f"{node.nodeUid}_stat")
                service = json.loads(service.decode('utf-8'))
                response = requests.delete(
                    'http:{}:{}/scheduler/node/{}/'.format(
                        service.get('node_host'),
                        service.get('node_port'),
                        task_uid
                    ),
                    params={
                        'token': service.get('token')
                    }
                )
                response.raise_for_status()
                if response.json().get('code') != Code.OK:
                    errors[node.nodeUid] = response.json().get('msg')
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

    @swagger_auto_schema(
        operation_summary='任务部署',
        operation_description='部署任务',
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
    def post(self, request: Request):
        """
        部署任务
            多次部署已经存在的任务的节点将不做处理，未部署的节点将完成部署流程
        """
        task_uid = request.query_params.get('taskUid')

        task = TaskModel.objects.get(taskUid=task_uid)
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
        errors = {}
        for node in nodes:
            try:
                service = conn.get(f"{node.nodeUid}_stat")
                service = json.loads(service.decode('utf-8'))
                response = requests.post(
                    'http:{}:{}/scheduler/node/'.format(
                        service.get('node_host'),
                        service.get('node_port')
                    ),
                    params={
                        'token': service.get('token')
                    },
                    data={
                        'taskUid': task_uid
                    }
                )
                response.raise_for_status()
                if response.json().get('code') != Code.OK:
                    errors[node.nodeUid] = response.json().get('msg')
            except Exception as e:
                errors[node.nodeUid] = str(e)
        return CustomResponse(
            code=Code.OK,
            msg='Success',
        )

    @swagger_auto_schema(
        operation_summary='任务重新部署',
        operation_description='重新部署任务',
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
    def put(self, request: Request):
        """
        重新部署任务
        """
        task_uid = request.query_params.get('taskUId')

        task = TaskModel.objects.get(taskUid=task_uid)
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
        errors = {}
        for node in nodes:
            try:
                service = conn.get(f"{node.nodeUid}_stat")
                service = json.loads(service.decode('utf-8'))
                response = requests.put(
                    'http:{}:{}/scheduler/node/{}/'.format(
                        service.get('node_host'),
                        service.get('node_port'),
                        task_uid
                    ),
                    params={
                        'token': service.get('token')
                    }
                )
                response.raise_for_status()
                if response.json().get('code') != Code.OK:
                    errors[node.nodeUid] = response.json().get('msg')
            except Exception as e:
                errors[node.nodeUid] = str(e)
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
        service = conn.get(f"{node_uid}_stat")
        service = json.loads(service.decode('utf-8'))
        token = service.get('token')
        response = requests.get(
            'http:{}:{}/scheduler/logs/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid,
            ),
            params={
                'token': token
            }
        )
        if response.json().get('code') != Code.OK:
            return CustomResponse(
                code=response.json().get('code'),
                msg=response.json().get('msg'),
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
        service = conn.get(f"{node_uid}_stat")
        service = json.loads(service.decode('utf-8'))
        token = service.get('token')
        response = requests.delete(
            'http:{}:{}/scheduler/logs/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid,
            ),
            params={
                'token': token
            }
        )
        if response.json().get('code') != Code.OK:
            return CustomResponse(
                code=response.json().get('code'),
                msg=response.json().get('msg'),
            )
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data=response.json().get('data')
        )
