# 世纪佳缘psot请求登录接口(post请求和模拟登录)
import requests

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
response = requests.post(url=url,data=formdata,headers=headers)
print(response.status_code)

#获取登录成功的cookies信息
cookiejar = response.cookies
print(cookiejar)
print(type(cookiejar)) #->RequestsCookieJar对象

#登录成功后，使用cookie访问个人主页
pageurl = 'http://www.jiayuan.com/196235559'

#方式一：
# cookie_dict = {} #key:cookie的名称，value：cookie的值
# for cookie in cookiejar:
#     print(cookie.name,cookie.value)
#     cookie_dict[cookie.name] = cookie.value
# cookies: (optional) Dict or CookieJar object
#方式二
cookie_dict = requests.utils.dict_from_cookiejar(cookiejar)
print(cookie_dict)

response = requests.get(url=pageurl,headers=headers,cookies=cookie_dict)

print(response.status_code)
with open('sjpage.html','w') as file:
    file.write(response.text)











