#https://httpbin.org/post测试接口,给服务器
# 什么数据就返回什么数据
from urllib import request,parse

url = 'https://httpbin.org/post'

form_data = {
    'className':'1808',
    'peopleNum':30,
    'names':['zhangsan','lisi','wangwu','zhaoliu']
}

#使用urlencode将上传的表单书数据转换为url编码格式(#className=1808&peopleNum=30.....),
#再将字符串转为bytes类型(使用encode)
b_form_data = parse.urlencode(form_data).encode('utf-8')
print(b_form_data)
#b'className=1808&names=%5B%27zhangsan%27%2C+%27lisi%27%2C+%27wangwu%27%2C+%27zhaoliu%27%5D&peopleNum=30'

response = request.urlopen(url=url,data=b_form_data)
print(response.status)
print(response.read().decode('utf-8'))



