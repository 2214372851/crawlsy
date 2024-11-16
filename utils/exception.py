class SchedulerException(Exception):
    """
    自定义异常
    """

    def __init__(self, msg):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return self.msg


class OpenApiException(Exception):
    """
    外部API异常
    """

    def __init__(self, msg):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return self.msg
