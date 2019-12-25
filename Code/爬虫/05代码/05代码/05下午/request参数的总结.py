import requests

requests.get()
requests.post()
requests.put()
requests.delete()
.....



无论是哪一种请求方式，内部都调用的 -> requests.request()


"""
request()方法的参数：

:param method: 设置请求的方式.
:param url: 请求的url地址.
:param params: (optional) Dictionary get请求后面拼接的参数
:param data: (optional) Dictionary ,post请求提交的数据
:param json: (optional) json data 要求是一个json数据，等价与data的作用
:param headers: (optional) Dictionary 设置请求头
:param cookies: (optional) Dict or CookieJar object 模拟用户登录的时候
:param files: (optional) Dictionary 上传文件
:param auth: (optional) Auth tuple  web客户端认证auth（账号，密码）
:param timeout: (optional) 设置请求超时时间
:param allow_redirects: (optional) Boolean. Defaults to ``True``.是否允许重定向
:param proxies: (optional) Dictionary 设置代理.
:param verify: Defaults to ``True``，ssl证书认证，默认为True，表示进行证书认证

"""