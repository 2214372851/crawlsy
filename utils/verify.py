import re


def is_username(value):
    pattern = re.compile(r'^[\u4E00-\u9FA5A-Za-z0-9_]+$')
    return bool(pattern.search(value))


def is_email(value):
    pattern = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
    return bool(pattern.search(value))


def is_password(value):
    pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d).{6,16}$')
    return bool(pattern.search(value))


def is_phone(value):
    pattern = re.compile(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$')
    return bool(pattern.search(value))
