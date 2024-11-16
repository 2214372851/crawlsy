import logging

from django.db.models import ProtectedError
from django.db.utils import IntegrityError
from jwt.exceptions import ExpiredSignatureError
from django.core.exceptions import ValidationError
from rest_framework.exceptions import (AuthenticationFailed, NotAuthenticated,
                                       PermissionDenied as RestPermissionDenied,
                                       ValidationError as DrfValidationError)
from rest_framework.views import exception_handler

from utils.code import Code
from utils.exception import SchedulerException, OpenApiException
from utils.response import CustomResponse

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
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
    if isinstance(exc, SchedulerException):
        return CustomResponse(
            code=Code.DATA_LOSS,
            msg=str(exc)
        )
    if isinstance(exc, DrfValidationError):
        return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg='数据不合法',
            data=exc.detail
        )
    if isinstance(exc, OpenApiException):
        return CustomResponse(
            code=Code.UNKNOWN,
            msg=str(exc)
        )
    if isinstance(exc, ValidationError):
        return CustomResponse(
            code=Code.INVALID_ARGUMENT,
            msg=exc.messages[0]
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
    if isinstance(exc, ValueError):
        return CustomResponse(
            code=Code.FAILED_PRECONDITION,
            msg=str(exc)
        )
    if isinstance(exc, FileNotFoundError):
        return CustomResponse(
            code=Code.NOT_FOUND,
            msg='资源不存在',
            data={'error': str(exc)},
        )
    if isinstance(exc, IntegrityError):
        return CustomResponse(
            code=Code.DATA_LOSS,
            msg='服务器内部错误',
            data={'error': str(exc)},
        )
    if isinstance(exc, Exception):
        logger.error(str(exc), str(context), exc_info=True)
        return CustomResponse(
            code=Code.INTERNAL,
            msg='服务器内部错误',
            data={'error': str(exc)}
        )
    return response
