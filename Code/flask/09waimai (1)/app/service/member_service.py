import requests
from config import Config
from flask import current_app
import json
import hashlib, string, random


class MemberService():

    @staticmethod
    def geneAuthCode(member_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def getOpenid(code):
        app_id = current_app.config.get('APP_ID')
        app_secret = current_app.config.get('APP_SECRET')
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code' \
            .format(app_id, app_secret, code)

        response = requests.get(url).json()

        openid = response.get('openid') if 'openid' in response else None

        return openid

    @staticmethod
    def getSalt(len=16):
        str = [random.choice(string.ascii_letters + string.digits) for _ in range(1, len + 1)]

        ran_str = "".join(str)

        return ran_str
