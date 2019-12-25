#web客户端认证：早期的网站会出现这中认证现象，
#目前访问内网资源的时候可能会出现这种认证

import requests

url = 'https://198.127.2.1'

auth = ('name','1234')

response = requests.get(url,auth=auth)

if response.status_code == 200:
    print('成功了')

