# 什么是代理？
# 代理就是代理服务器（proxy server）,存在的目的：
# 代理网络用户访问服务器获取数据
#
# 为什么使用代理？
# 因为在爬虫爬取数据的过程中，如果提高爬取效率，往往会
# 导致访问服务器频率过快，超过对方服务器设置的频率阀值，
# 就可能认为你是一个违规用户（爬虫），会封掉你的ip（封ip
# 并不是一个永久行为）

# 如何设置代理？
#因为urlopen方法并不能设置代理，所以我们需要自定义opener

from urllib import request
import ssl
#创建处理器
"""
proxies:对应的是一个字典类型
常用的是http/https代理服务器
并且要是高匿代理

代理的获取途径：
免费：西刺代理、快代理、讯代理 （质量不高）
收费代理：西瓜代理、快代理、讯代理、芝麻代理、阿布云代理 （质量高）
"""
proxies = {
    'https':'60.190.250.120:8080',
    'http':'121.61.3.209:9999',
    'https':'username:password@60.190.250.120:8080'#有账号密码的代理
}


proxy_handler = request.ProxyHandler(proxies=proxies)
https_handler = request.HTTPSHandler(debuglevel=1,context=ssl._create_unverified_context())
http_handler = request.HTTPHandler(debuglevel=1)
#根据handler，自定义opener
opener = request.build_opener(proxy_handler,https_handler,http_handler)

# url = 'https://www.baidu.com/'

# url = 'http://www.jiayuan.com/'

url = 'http://httpbin.org/get'

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}

req = request.Request(url,headers=headers)


#发起请求
# response = opener.open(req)
request.install_opener(opener)
response = request.urlopen(req)

print(response.status)
print(response.read().decode('utf-8'))







