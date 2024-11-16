from rest_framework.response import Response
from utils.code import Code


class CustomResponse(Response):
    def __init__(self, code: Code, msg: str, data=None, status=200, headers=None, **kwargs) -> None:
        response_data = {
            'code': code.value,
            'msg': msg,
        }
        if data is not None: response_data['data'] = data
        response_data.update(kwargs)
        super().__init__(data=response_data, status=status, headers=headers,
                         exception=False, content_type=None)

