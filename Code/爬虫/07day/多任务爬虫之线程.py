#队列的使用：
# 在线程中多用队列作为数据交换的方式，

# 因为队列是线程安全的，python原声的lits
# ，dict是非线程安全的，需要跟线程锁配合使用，
# 所以正式因为队列是线程安全的，所以在线程中
# 多用队列作为数据交换的方式，

# import queue
#
# #实例化一个队列(先进先出FIFO)
# #maxsize设置队列存放数据的最大值
# que = queue.Queue(maxsize=50)
#
# for i in range(0,50):
#     #put()方法往队列中存值
#     que.put(i)
#
# print(que.full()) #判断队列是否满了
# print(que.empty()) #判断队列是否为空
# print(que.qsize()) #获取大小
#
# while not que.empty():
#     print(que.get())


import queue,requests,json
import pymongo,pymysql
import threading
from requests import exceptions
from lxml import etree

def crawlTaskRequest(taskQueue,dataQueue):
    """
    分析：
    发起请求，需要任务队列taskQueue，从任务队列中取任务
    存储获取的页面源码需要数据队列，dataQueue
    :return:
    """
    while not taskQueue.empty():
        pagenum = taskQueue.get()
        print('正在爬取'+str(pagenum)+'页',threading.currentThread().name)
        fullUrl = 'https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page='+str(pagenum)
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }
        try:
            response = requests.get(url=fullUrl,headers=headers)
            if response.status_code == 200:
                html = response.text
                #将获取的页面源码，放入数据队列
                dataQueue.put(html)
        except exceptions.HTTPError as err:
            print(err)
        except exceptions.ConnectTimeout as err:
            print(err)
        except exceptions.RequestException as err:
            print(err)


def parsePageData(dataQueue,lock):

    while not dataQueue.empty():
        print('正在解析数据',threading.currentThread().name)
        #从队列中获取html页面源码
        html = dataQueue.get()
        #解析数据(实例化一个xpath的解析对象)
        x_html = etree.HTML(html)
        #获取菜谱列表
        caipu_list = x_html.xpath('//div[@class="listtyle1"]')

        for caipu_div in caipu_list:
            item = {}
            #封面图片
            item['coverImage'] = caipu_div.xpath('.//img[@class="img"]/@src')[0]
            #类型
            item['type'] = caipu_div.xpath('.//strong[@class="gx"]/span/text()')
            if len(item['type']) > 0:
                item['type'] = item['type'][0]
            else:
                item['type'] = '暂无'

            #标题
            item['title'] = caipu_div.xpath('.//div[@class="c1"]/strong/text()')[0]

            lock.acquire() #加锁
            with open('caipilist.json','a+') as file:
                json_str = json.dumps(item,ensure_ascii=False) + '\n'
                file.write(json_str)
            lock.release() #解锁




if __name__ == '__main__':

    #任务队列（存放任务）
    taskQueue = queue.Queue()
    #https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page=1
    #https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page=2
    #https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page=3
    for page in range(1,57):
        taskQueue.put(page)

    # 数据队列（存放爬取线程获取的页面源码数据）
    dataQueue = queue.Queue()

    #爬取线程（执行下载任务）
    crawlThreads = []
    for i in range(1,5):
        crawlThread = threading.Thread(
            target=crawlTaskRequest,
            args=(taskQueue,dataQueue),
            name='crawl%s' % str(i)
        )
        crawlThread.start()
        crawlThreads.append(crawlThread)

    #爬取线程设置阻塞，等待任务队列中的任务爬取完毕
    for thread in crawlThreads:
        thread.join()


    lock = threading.Lock()
    #解析线程（将数据队列中的页面源码数据取出来，解析）
    parseThreads = []
    for i in range(1,5):
        parseThread = threading.Thread(
            target=parsePageData,
            args=(dataQueue,lock),
            name='parse%s' % str(i)
        )
        parseThread.start()
        parseThreads.append(parseThread)

    # 解析线程设置阻塞，等待数据队列中的页面源码解析完毕
    for thread in parseThreads:
        thread.join()

    #数据持久化







