import json
import logging
from concurrent.futures import ThreadPoolExecutor

from django.utils.datetime_safe import datetime
from requests import request

from utils.exception import OpenApiException

logger = logging.getLogger('django')


class FeishuApi:
    """飞书开放平台API"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.authorization = f'Bearer {self.get_tenant_access_token()}'

    def get_tenant_access_token(self):
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        # "application/json; charset=utf-8"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        try:
            response = request('POST', url, json={'app_id': self.app_id, 'app_secret': self.app_secret},
                               headers=headers)
            response.raise_for_status()
            response_data = response.json()
            if response_data['code'] == 0:
                return response_data['tenant_access_token']
            else:
                raise OpenApiException(response_data['msg'])
        except Exception as e:
            logger.error(e, exc_info=True)
            raise OpenApiException('网络异常稍后重试')

    def get_users_id(self, *args: [str]) -> dict:
        url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=user_id'
        headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': self.authorization}
        try:
            response = request(
                'POST', url,
                json={
                    "emails": args,
                    "include_resigned": True
                },
                headers=headers
            )
            response.raise_for_status()
            response_data = response.json()
            if response_data['code'] == 0:
                user_list = response_data['data']['user_list']
                result = {}
                for user in user_list:
                    result[user['email']] = user.get('user_id', None)
                return result
            else:
                raise OpenApiException(response_data['msg'])
        except Exception as e:
            logger.error(e, exc_info=True)
            raise OpenApiException('网络异常稍后重试')

    def send_message(
            self,
            users_id: [str], msg: str, severity: str,
            interval: int, callback_url: str,
            card_id: str, card_version: str
    ):
        users = [user for user in users_id if user]
        url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id'
        color = self.get_color(severity)
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': self.authorization,

        }
        content = {
            "type": "template",
            "data": {
                "template_id": card_id,
                "template_version_name": card_version,
                "template_variable": {
                    "alertUsers": users,
                    "msg": msg,
                    "severity": severity,
                    "color": color,
                    "interval": str(interval),
                    "callbackUrl": callback_url,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        }

        def _send(send_id: str):
            try:
                response = request(
                    'POST',
                    url,
                    json={
                        "receive_id": send_id,
                        "msg_type": "interactive",
                        "content": json.dumps(content)
                    },
                    headers=headers
                )
                response.raise_for_status()
                response_data = response.json()
                if response_data['code'] == 0:
                    return True
                else:
                    logger.error(response_data['msg'], exc_info=True)
                    raise OpenApiException('请检查飞书是否绑定邮箱')
            except Exception as e:
                logger.error(e, exc_info=True)
                raise OpenApiException('网络异常稍后重试')

        fultures = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            for user_id in users:
                fultures.append(executor.submit(_send, user_id))
        for f in fultures:
            if f.exception():
                logger.error(f.exception())
                raise f.exception()

    def send_webhook(
            self, url: str, users_id: [str], msg: str,
            severity: str, interval: int, callback_url: str,
            card_id: str, card_version: str
    ):
        users = [user for user in users_id if user]
        color = self.get_color(severity)
        data = {
            "msg_type": "interactive",
            "card": {
                "type": "template",
                "data": {
                    "template_id": card_id,
                    "template_version_name": card_version,
                    "template_variable": {
                        "alertUsers": users,
                        "msg": msg,
                        "severity": severity,
                        "color": color,
                        "interval": str(interval),
                        "callbackUrl": callback_url,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            }
        }
        try:
            response = request(
                'POST',
                url,
                data=json.dumps(data, ensure_ascii=False),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            response_data = response.json()
            if response_data['code'] == 0:
                return True
            else:
                logger.error(response_data['msg'], exc_info=True)
                raise OpenApiException('推送失败')
        except Exception as e:
            logger.error(e, exc_info=True)
            raise OpenApiException('网络异常稍后重试')

    @staticmethod
    def get_color(severity):
        return {"critical": 'red', 'warning': 'orange', 'info': 'blue'}.get(severity, 'orange')


if __name__ == '__main__':
    from crawlsy import settings

    fs = FeishuApi('cli_a7b2a9e17f3dd013', '4PC9uWLh1mS4LFl1qvIpFfFUqRfnokWi')
    user_id = fs.get_users_id('bybxbwg@foxmail.com', '2214372851@qq.com')
    fs.send_message(
        users_id=user_id.values(),
        msg='测试消息', severity='low', interval=60, callback_url='https://127.0.0.1',
        card_id=settings.CARD_ID, card_version=settings.CARD_VERSION
    )
