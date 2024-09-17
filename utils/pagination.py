import math

from rest_framework.pagination import PageNumberPagination

from utils.code import Code
from utils.response import CustomResponse


class CustomPagination(PageNumberPagination):
    """
    自定义分页器类
    """
    page_size = 10
    page_query_param = 'page'
    max_page_size = 30
    page_size_query_param = 'pageSize'

    def get_paginated_response(self, data):
        return CustomResponse(
            code=Code.OK,
            msg='Success',
            data={
                'total': self.page.paginator.count,
                'list': data
            })
