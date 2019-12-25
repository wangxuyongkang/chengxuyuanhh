#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()
    #
    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        response = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)

        return response.json()

#
if __name__ == '__main__':

	chaojiying = Chaojiying_Client('18518753265', 'ljh12345678', '898122')	#用户中心>>软件ID 生成一个替换 96001
	im = open('caption_image.png', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
	print(chaojiying.PostPic(im, 9004))											#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    # import json
    #
    # str = '{"pic_str": "158,238|173,137"}'
    # data = json.loads(str)
    #
    # pic_str = data['pic_str'].split("|")
    #
    # location = [[location for location in pic_location.split("|")]for pic_location in pic_str]
    # print(location)