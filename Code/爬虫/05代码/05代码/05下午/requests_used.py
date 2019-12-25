# 为什么要学习和使用requests?
# requests是基于urllib的再一次封装，
# 具有urllib的一切特性，并且API调用更加方便

#安装
# pip3 install requests
import requests

#requests发起一个get请求
"""
url:要请求的URL地址
params：dict类型，get请求url地址后拼接的参数
headers: dict类型 设置请求头
timeout设置请求的超时时间
"""
url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?"
parmas = {
    'since_id':'-1',
    'max_id':'-1',
    'count':'10',
    'category':'6',
    '123':'中午问'
}
#请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
response = requests.get(url=url,params=parmas,headers=headers,timeout=10)

#获取响应的状态码
code = response.status_code
print(code)
#获取响应的二进制数据
content = response.content
content_str = content.decode('utf-8')
print(content)
print(content_str)
#直接获取响应结果的text文本
# (注意如果response.text
# 获取的页面数据出现乱码的情况，我们可以
# content = response.content
# content_str = content.decode('utf-8')
# 进行解码操作)
text = response.text
print(text)
#获取响应的头部
response_headers = response.headers
print(response_headers)
#获取请求的请求头
request_headers = response.request.headers
print(request_headers)
#获取当前请求的url地址
current_url = response.url
print(current_url)
#response.json() => json.loads(response.text)
#可以将json字符串转换为python数据类型
json_data = response.json()
print(json_data)
print(type(json_data))






