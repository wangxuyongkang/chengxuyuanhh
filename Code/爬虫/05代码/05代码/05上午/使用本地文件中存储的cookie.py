"""
MozillaCookieJar (filename,delayload=None,policy=None)：从FileCookieJar派生而来，创建与Mozilla浏览器 cookies.txt兼容的FileCookieJar实例。
"""

from urllib import request,parse
from http.cookiejar import CookieJar,MozillaCookieJar
import ssl

#管理HTTP cookie值、存储HTTP请求生成的cookie,将cookie信息
#保存在内存中
filename = 'cookie.txt'
cookjar = MozillaCookieJar(filename=filename)

#加载本地保存的cookie信息
cookjar.load(filename=filename)

#创建handler处理器
handle = request.HTTPCookieProcessor(cookjar)

https_handler = request.HTTPSHandler(debuglevel=1,context=ssl._create_unverified_context())

#自定义 opener
opener = request.build_opener(handle,https_handler)

#发起请求
#个人主页
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}
url = 'http://www.jiayuan.com/196235559'

req = request.Request(url,headers=headers)

response = opener.open(req)

if response.status == 200:
    with open('jiayuan.html','w') as file:
        file.write(response.read().decode('utf-8'))
