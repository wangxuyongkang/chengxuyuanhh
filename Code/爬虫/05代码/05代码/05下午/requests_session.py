# requests库中的session作用：
# 维持同一会话，在跨请求访问的时候能够保存一些参数信息（比如cookies）

import requests

#创建session对象，支持跨请求访问
cus_session = requests.session()

url = 'https://passport.jiayuan.com/dologin.php?pre_url=http://www.jiayuan.com/usercp'

"""
name: 18518753265
password: 123
remem_pass: on
_s_x_id: 1e56aee116b168e393cf4591b48c44a2
ljg_login: 1
m_p_l: 1
channel: 
position: 
"""
#需要提交的表单数据
formdata = {
    'name': '18518753265',
    'password': 'ljh123456',
    'remem_pass': 'on',
    '_s_x_id': '1e56aee116b168e393cf4591b48c44a2',
    'ljg_login': '1',
    'm_p_l': '1',
    'channel':'',
    'position':'',
}

"""
url:要请求的url地址
data：要提交的表单数据（post请求需要提交的数据）
"""
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
response = cus_session.post(url=url,data=formdata,headers=headers)
print(response.status_code)

if response.status_code == 200:
    # 登录成功后，使用cookie访问个人主页
    pageurl = 'http://www.jiayuan.com/196235559'

    response = cus_session.get(url=pageurl,headers=headers)

    if response.status_code == 200:
        with open('page.html','w') as file:
            file.write(response.text)
