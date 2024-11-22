import logging

from rest_framework.request import Request
from rest_framework.views import APIView

from apps.Task.models import TaskModel
from utils.code import Code
from utils.response import CustomResponse
from utils.mongo_pool import mongodb_pool
from bson.json_util import dumps
import json

logger = logging.getLogger('django')


class TaskResultView(APIView):
    """
    任务结果
    """

    def get(self, request: Request):
        """
        获取任务结果
        :param request:
        :return:
        """
        task_id = request.query_params.get('id')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 10))
        if not task_id:
            return CustomResponse(msg='参数错误', code=Code.INVALID_ARGUMENT)
        task: TaskModel = TaskModel.objects.filter(id=task_id).first()
        if not task:
            return CustomResponse(msg='任务不存在', code=Code.NOT_FOUND)
        collection = mongodb_pool.collection(str(task.taskUid))
        task_result = (collection
                       .find()
                       .skip((page - 1) * page_size)
                       .sort('_id', -1)
                       .limit(page_size))
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data={
                'total': collection.count_documents({}),
                'list': json.loads(dumps(task_result))
            })
