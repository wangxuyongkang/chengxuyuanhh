from urllib import request
import re
# http://top.hengyan.com/dianji/default.aspx?p=2
url = 'http://top.hengyan.com/dianji/default.aspx?p=1'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3738.400'
}
#url, \目标url
# data=None, \默认为None表示是get请求,如果不为None说明是get请求
# timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
#            *, cafile=None, capath=None, cadefault=False,
#            context=None 忽略证书
#urlopen 不能添加请求头
#添加请求头
req = request.Request(headers=headers,url=url)
#请求req
response = request.urlopen(url=req,timeout=10)

code = response.status
url = response.url
#转换为二进制
b_content = response.read()
#二进制转换为字符串 decode
html = b_content.decode('utf-8')
#字符转转换为二进制 incode

#文件操作
'''
w：写入    w+: 追加写入    wb: 二进制    wb+:     a： 追加写入  a+：  ab   ab+   r    rb
'''

# with open('hengyan.html','w',encoding='utf-8') as file:
#     file.write(html)
#
# print(code,url)
# print(html)
#根据正则表达式解析数据
#re.S 修饰: 表示可以匹配换行符
pattern = re.compile('<div\sclass="list">(.*?)</div>',re.S)

pattern1 = re.compile('<ul.*?>(.*?)</ul>',re.S)
li_strs = re.findall(pattern1)
# pattern = re.compile(
#     '<ul>.*?<li\sclass="num">(.*?)</li>'+
#     '.*?<a.*?>(.*?)</a>'+
#     '.*?<li .*?>(.*?)</li>'+
#     '.*?<li .*?>(.*?)</li>'+
#     '.*?<li .*?>(.*?)</li>'+
#     '.*?<li .*?>(.*?)</li>.*?</ul>',
#     re.S
# )
data = re.findall(pattern=pattern,string=html)
print(data)
for item in data:
    print(item)