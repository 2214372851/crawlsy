from enum import IntFlag


class Status(IntFlag):
    # 运行中
    RUNNING = 1
    # 停止
    STOP = 2
    # 错误
    ERROR = 4
    # 不存在
    NOT_EXIST = 8
    # 离线
    OFFLINE = 16