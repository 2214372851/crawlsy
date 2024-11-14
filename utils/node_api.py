import json

import requests

from utils.code import Code


class NodeApi:

    @staticmethod
    def node_task_stat(service, node_uid, task_uid) -> requests.Response:
        response = requests.get(
            'http://{}:{}/scheduler/node/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid
            ),
            params={
                'token': node_uid
            }
        )
        response.raise_for_status()
        return response

    @staticmethod
    def node_task_stop(conn, node_uid, task_uid):
        service = conn.get(f"{node_uid}_stat")
        if not service:
            return
        service = json.loads(service.decode('utf-8'))
        response = requests.delete(
            'http://{}:{}/scheduler/node/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid
            ),
            params={
                'token': service.get('token')
            }
        )
        response.raise_for_status()
        if response.json().get('code') != Code.OK.value:
            raise RuntimeError(response.json().get('msg'))

    @staticmethod
    def node_task_start(conn, node_uid, task_uid):
        service = conn.get(f"{node_uid}_stat")
        service = json.loads(service.decode('utf-8'))
        response = requests.post(
            'http://{}:{}/scheduler/node/'.format(
                service.get('node_host'),
                service.get('node_port')
            ),
            params={
                'token': service.get('token')
            },
            json={
                'taskUid': task_uid,
                'command': 'ping baidu.com'
            }
        )
        response.raise_for_status()
        if response.json().get('code') != Code.OK.value:
            raise RuntimeError(response.json().get('msg'))

    @staticmethod
    def node_task_reload(conn, node_uid, task_uid):
        service = conn.get(f"{node_uid}_stat")
        service = json.loads(service.decode('utf-8'))
        response = requests.put(
            'http://{}:{}/scheduler/node/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid
            ),
            params={
                'token': service.get('token')
            },
            json={
                'command': 'ping baidu.com'
            }
        )
        response.raise_for_status()
        if response.json().get('code') != Code.OK.value:
            raise RuntimeError(response.json().get('msg'))

    @staticmethod
    def node_task_start_log(conn, node_uid, task_uid) -> requests.Response:
        service = conn.get(f"{node_uid}_stat")
        service = json.loads(service.decode('utf-8'))
        response = requests.get(
            'http://{}:{}/scheduler/logs/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid
            ),
            params={
                'token': service.get('token')
            }
        )
        response.raise_for_status()
        if response.json().get('code') != Code.OK.value:
            raise RuntimeError(response.json().get('msg'))
        return response

    @staticmethod
    def node_task_stop_log(conn, node_uid, task_uid) -> requests.Response:
        service = conn.get(f"{node_uid}_stat")
        service = json.loads(service.decode('utf-8'))
        response = requests.delete(
            'http://{}:{}/scheduler/logs/{}/'.format(
                service.get('node_host'),
                service.get('node_port'),
                task_uid
            ),
            params={
                'token': service.get('token')
            }
        )
        response.raise_for_status()
        if response.json().get('code') != Code.OK.value:
            raise RuntimeError(response.json().get('msg'))
        return response
