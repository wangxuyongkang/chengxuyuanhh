# urlopen()
# 什么是opener？
# opener是 urllib.request.OpenerDirector 的实例
# 我们经常使用的 urlopen方法内部其实就是自定义了opener
#
# 为什么要自定义opener?
# 因为urlopen方法比较有局限性，不能够实现一些高级的功能
# (使用代理，处理cookies)，这时我们就需要自定义opener
# 去实现这些功能

#handler：处理器，实例化一个 handler的目的是为了完成特定
# 的功能

#install_opener():将自定义的opener设置为全局的opener,
#下次直接调用urlopen方法的时候使用的就是自定义的opener


from urllib import request
import ssl

#自定义 opener

# request.urlopen()

#自定义handler
#debuglevel=1 :在发起请求的时候可以打印请求的报头信息（调试模式）
# handler:有调试模式，可以忽略证书认证，可以发起https 请求
handler = request.HTTPSHandler(debuglevel=1,context=ssl._create_unverified_context())

#实例化opener
opener = request.build_opener(handler)

url = 'https://www.baidu.com/'

#  最终调用open()发起请求
# response = opener.open(url)

#可以将自定义的opener设置为全局的opener
request.install_opener(opener)

response = request.urlopen(url)

if response.status == 200:
    print('请求成功')

