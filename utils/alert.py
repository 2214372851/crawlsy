import json
from uuid import uuid4

import requests


def feishu_webhook():
    web_hook_url = ''
    alert_title = ''
    requests.get(web_hook_url)


json_data = {
    "receive_id": "oc_d27abf52f81967c8f4e65d08cc703d31",
    "msg_type": "interactive",
    "content": json.dumps({
        "type": "template",
        "data": {
            "template_id": "AAqCfYzThjx4O",
            "template_variable":
                {
                    "node": "测试节点",
                    "date": "测试节点",
                    "tasks": "测试节点",
                    "users": "测试节点",
                    "msg": "测试节点",
                }
        }
    }, ensure_ascii=False),
    "uuid": str(uuid4())
}

headers = {
    'Authorization': 'Bearer t-g1048g9tLYQZYA6TQKVIW2347J6HT23S5B6GEDLM'
}
data = requests.post('https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id', json=json_data,
                     headers=headers)
print(data, data.text)
