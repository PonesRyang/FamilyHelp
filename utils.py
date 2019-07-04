import hashlib
import json
import random

import requests

ALL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def random_captcha_text(length=4):
    """生成随机验证码字符串"""
    return ''.join(random.choices(ALL_CHARS, k=length))


def random_mobile_code(length=6):
    """生成随机短信验证码"""
    return ''.join(random.choices('0123456789', k=length))


def send_code_by_sms(tel, code):
    """发送验证码短信"""
    resp = requests.post(
        "http://sms-api.luosimao.com/v1/send.json",
        auth=("api", "key-8369a8899b6c8bce7944486fc0e73c63"),
        data={
            "mobile": tel,
            "message": f"您的短信验证码是{code}，打死也不能告诉别人哦【铁壳测试】"
        },
        timeout=5,
        verify=False)
    return json.loads(resp.content)