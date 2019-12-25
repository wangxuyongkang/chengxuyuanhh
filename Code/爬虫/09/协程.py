# 什么叫可迭代对像。
# 迭代是访问集合元素的一种方式，可以使用for循环的对象都是
# 可迭代对象（list，tuple，dict，set，str）
from collections import Iterable
data = 1
print(isinstance(data,Iterable))

data = ['1','2','3','4','5']
# for i in data:
#     print(i)

n_data = iter(data)
#
# print(next(n_data))
# print(next(n_data))
# print(next(n_data))


#什么是迭代器？
#迭代器是一个可以记住遍历位置的对象,__iter__,__next__;
from collections import Iterator
print(isinstance(n_data,Iterator))

class getNum(object):
    def __init__(self,num):
        self.num = num
        self.currentNum = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.currentNum < self.num:
            self.currentNum += 1
            return self.currentNum
        else:
            raise StopIteration

classNum = getNum(100)
print(type(classNum))
print(isinstance(classNum,Iterator))

print(next(classNum))

for i in getNum(10):
    print(i)


# 什么是生成器？
# 生成器是一个特殊的迭代器，内部保留的是一段算法，一边执行一边运算
# 创建生成器的方式
# 方式一
objData = (i for i in (1,2,3,4,5,6,7,8,9) if i > 5)
#generator object(生成器对象)
print(objData)
# 方式二

def getNum(num):
    currentNum = 0
    while currentNum < num:
        currentNum += 1
        yield currentNum


# 一个方法里面一旦出现了yield关键字，那么这个方法就不再
# 是一个方法了,这是候就是一个生成器。
# yield:
# 第一点能够当村当前的运行状态，然后暂停执行。
# 第二点yield后面的值会返回给我们,相当于returen的作用
#
# 下一个调用next()方法的时候会接着之前暂停的位置继续执行


objData = getNum(10)

print(next(objData))
print(next(objData))

#什么是协程？
# 是除了线程、进程之外实现多任务的另一种方式，协程比线程暂用的资源
# 更少，拥有cpu寄存器上下文,这样协程和协程之间任务切换就会非常块

def homework1():
    while True:
        print('do homework1')
        yield '1'

def homework2():
    while True:
        print('do homework2')
        yield '2'

h1 = homework1()
h2 = homework2()
#
# while True:
#     next(h1)
#     next(h2)


#使用三方库实现协程
# pip3 install greenlet
# pip3 install gevent
import requests
from greenlet import greenlet
def download_data1(url):
    print('正在下载图片1')
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    #https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg
    response = requests.get(url=url,headers=headers)

    grelet2.switch('https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg')

    if response.status_code == 200:
        print('正在执行图片1的写入操作')
        with open('image1.jpg','wb') as f:
            f.write(response.content)
    grelet2.switch()


def download_data2(url):
    print('正在下载图片2')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    # https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg
    response = requests.get(url=url, headers=headers)

    grelet1.switch()

    if response.status_code == 200:
        print('正在执行图片2的写入操作')
        with open('image2.jpg', 'wb') as f:
            f.write(response.content)

grelet1 = greenlet(download_data1)
grelet2 = greenlet(download_data2)

#switch()使用switch进行协程之间的切换
grelet1.switch('https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg')

# 虽然greenlet能够实现协程，但是任务切换需要手动完成，
# 切换的时机很难把控，我们可以使用gevent，内部可以实现
# 协程的自动切换
#pip3 install gevent
import gevent

def down_load(num):
    print('正在执行下载任务',num)
    gevent.sleep(1)
    print('下载任务完成', num)

gev1 = gevent.spawn(down_load,1)
gev2 = gevent.spawn(down_load,2)
gev3 = gevent.spawn(down_load,3)
gev4 = gevent.spawn(down_load,4)

gev1.join()
gev2.join()
gev3.join()
gev4.join()

# 协程池
from gevent import pool,monkey

#打补丁(将程序中的耗时操作代码，使用gevent自己的模块实现)
monkey.patch_all()

def download_data1(url):
    print('正在下载图片1')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    # https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        print('正在执行图片1的写入操作')
        with open('image1.jpg', 'wb') as f:
            f.write(response.content)

def download_data2(url):
    print('正在下载图片2')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }

    # https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        print('正在执行图片2的写入操作')
        with open('image2.jpg', 'wb') as f:
            f.write(response.content)

gevPool = pool.Pool(10)

gevent.joinall(
    [
        gevPool.spawn(download_data1,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
        gevPool.spawn(download_data2,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
        gevPool.spawn(download_data1,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
        gevPool.spawn(download_data2,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
        gevPool.spawn(download_data1,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
        gevPool.spawn(download_data2,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
        gevPool.spawn(download_data1,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
        gevPool.spawn(download_data2,'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=4102543213,3445727557&fm=27&gp=0.jpg'),
    ]
)










