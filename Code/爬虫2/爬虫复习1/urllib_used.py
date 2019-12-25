from urllib import request
# # http://top.hengyan.com/dianji/default.aspx?p=2
# url = 'http://top.hengyan.com/dianji/default.aspx?p=1'
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3738.400'
# }
# #url, \目标url
# # data=None, \默认为None表示是get请求,如果不为None说明是get请求
# # timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
# #            *, cafile=None, capath=None, cadefault=False,
# #            context=None 忽略证书
# #urlopen 不能添加请求头
# #添加请求头
# req = request.Request(headers=headers,url=url)
# #请求req
# response = request.urlopen(url=req,timeout=10)
#
# code = response.status
# url = response.url
# #转换为二进制
# b_content = response.read()
# #二进制转换为字符串 decode
# html = b_content.decode('utf-8')
# #字符转转换为二进制 incode
#
# #文件操作
# '''
# w：写入    w+: 追加写入    wb: 二进制    wb+:     a： 追加写入  a+：  ab   ab+   r    rb
# '''
#
# with open('hengyan.html','w',encoding='utf-8') as file:
#     file.write(html)
#
# print(code,url)
# print(html)
from urllib import parse,error
import json
###################POST请求##################
#http://search.jiayuan.com/v2/search_v2.php
#世纪佳缘
def get_sjjy_data(page=1,timeout=0.01):
    url = 'http://search.jiayuan.com/v2/search_v2.php'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3738.400'
    }
    '''
    sv: 1
    p: 1(页码)
    f: select
    listStyle: bigPhoto
    pri_uid: 0
    jsversion: v5
    '''
    form_data = {
        'sex':'f',
        'key':'',
        'stc':'1:11,2:20.28,23:1',
        'sv':1,
        'p':str(page),
        'f':'select',
        'listStyle':'bigPhoto',
        'pri_uid':0,
        'jsversion': 'v5',
    }
    for_data = parse.urlencode(form_data).encode('utf-8')
    #b'sex=f&key=&stc=1%3A11%2C2%3A20.28%2C23%3A1&sv=1&p=1&f=select&listStyle=bigPhoto&pri_uid=0&jsversion=v5'
    req = request.Request(headers=headers,url=url,data=for_data)

    try:
        response = request.urlopen(req,timeout=timeout)


        if response.status == 200:
            content = response.read().decode('utf-8').replace('##jiayser##//','').replace('##jiayser##','')
            data = json.loads(content)

            print(type(data),data)
            userinfos = data['userInfo']
            # page = data['pageTotal']
            for user in userinfos:
                age = user['age']
                name = user['nickname']
                gender = user['sex']
                print(age,name,gender)
            #获取下一页
            total_url = int(data['pageTotal'])
            print(str(page),'数据提取完毕')
            if page < total_url:
                #需要继续提取下一页
                next_page = page+1
                #递归方式 继续提取下一页数据
                get_sjjy_data(page=next_page)
            else:
                #数据提取完毕
                print('数据提取完毕')
        # json.load()#将本地文件中json字符转,转换成python数据类型(dict)
        # json.loads()son字符转,转换成python数据类型(dict)
        # json.dump()#将python数据类型转换为json字符串,并保存至本地文件
        # json.dumps():将python数据类型转换为json字符串
    except error.HTTPError as err:
        print(err.code)
        print(err.reason)
        print(err.headers)
        get_sjjy_data(page,timeout=10)
    except error.URLError as err:
        print(err.reason)

######################证书错误################
import ssl

url = 'https://wwww.baidu.com/'
#忽略证书
context = ssl._create_unverified_context()
response = request.urlopen(url=url,context=context)
if response.status == 200:
    print('请求成功')

# if __name__ == '__main__':
#     get_sjjy_data()
#################使用urllib请求添加代理#############
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3738.400'
}
proxy = {
    'http':'192.168.1.22.8000',
    'https':'192.168.1.22.80800'
}
#创建代理处理器
proxy_headler = request.ProxyHandler(proxies=proxy)
#自定义opener
opener = request.build_opener(proxy_headler)
req = request.Request(url=url,headers=headers)

response = opener.open(req)
print(response.code)