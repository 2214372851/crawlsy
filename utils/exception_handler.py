import logging

from django.db.models import ProtectedError
from django.db.utils import IntegrityError
from jwt.exceptions import ExpiredSignatureError
from rest_framework.exceptions import (AuthenticationFailed, NotAuthenticated,
                                       PermissionDenied as RestPermissionDenied,
                                       ValidationError)
from rest_framework.views import exception_handler

from utils.code import Code
from utils.response import CustomResponse

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(exc)
    logger.error(str(exc), str(context), exc_info=True)
    print(type(exc))
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return CustomResponse(
            code=Code.UNAUTHENTICATED,
            msg=str(exc)
        )
    if isinstance(exc, RestPermissionDenied):
        return CustomResponse(
            code=Code.PERMISSION_DENIED,
            msg=str(exc)
        )
    if isinstance(exc, ValidationError):
        return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg='数据不合法',
            data=exc.detail
        )
    if isinstance(exc, ExpiredSignatureError):
        return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg='身份信息失效',
        )
    if isinstance(exc, ProtectedError):
        return CustomResponse(
            code=Code.FAILED_PRECONDITION,
            msg='数据被使用中无法操作',
            data={'error': str(exc)},
        )
    if isinstance(exc, IntegrityError):
        return CustomResponse(
            code=Code.DATA_LOSS,
            msg='服务器内部错误',
            data={'error': str(exc)},
        )
    if isinstance(exc, Exception):
        return CustomResponse(
            code=Code.INTERNAL,
            msg='服务器内部错误',
            data={'error': str(exc)}
        )
    return response
