from croniter import croniter
from django.core.exceptions import ValidationError


def validate_cron(value):
    """
    校验 cron 表达式
    """
    return croniter.is_valid(value)
