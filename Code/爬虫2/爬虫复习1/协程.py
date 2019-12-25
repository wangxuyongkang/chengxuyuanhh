# 1.可迭代对象？
#判断是否是可迭代对象
from collections import Iterable
data = [1,2,3,4,5]
print(isinstance(data,Iterable))
# 2.迭代器？
# 迭代器内部有__iter__和__next__这两个方法
# 3.生成器？
# 4.协程？

#使用yield实现协程
from greenlet import greenlet
import requests
#
# def download1(url):
#     print(url,'download1开始请求')
#     response = requests.get(url)
#     if response.status_code == 200:
#         print('download1请求成功')
# def download2(url):
#     print(url,'download2开始请求')
#     response = requests.get(url)
#     if response.status_code == 200:
#         print('download2请求成功')
# #使用greenlet创建协程
# gl1 = greenlet(download1)
# gl2 = greenlet(download2)
# #switch完成协程之间的切换
# gl1.switch('https://www.baidu.com/')

##########################gevent#########
import gevent
def download1(url):
    print(url,'download1开始请求')
    response = requests.get(url)
    if response.status_code == 200:
        print('download1请求成功')


##创建协程
gl1 = gevent.spawn(download1,'https://www.baidu.com/?p=1')
gl2 = gevent.spawn(download1,'https://www.baidu.com/?p=2')
gl3 = gevent.spawn(download1,'https://www.baidu.com/?p=3')
gl1.join()
gl2.join()
gl3.join()

###########协程池##########
#monkey
from gevent import monkey,pool
monkey.patch_all()#打补丁,让耗时操作转换为gevent内部能够识别那些耗时和不耗时

pool = pool.Pool(4)
def download1(url):
    print(url,'download1开始请求')
    response = requests.get(url)
    if response.status_code == 200:
        print('download1请求成功')
gevent.joinall(
    [
        gevent.spawn(download1,'https://www.baidu.com/?p=1')
    ]
)
