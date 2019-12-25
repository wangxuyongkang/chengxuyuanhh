import queue,requests,json
import pymongo,pymysql
import threading
from requests import exceptions
from lxml import etree
import os
import time

from multiprocessing import Process,Queue

#任务队列
#爬取进程
#数据队列
#解析进程

def crawlTaskRequest(taskQueue,dataQueue):
    """
    分析：
    发起请求，需要任务队列taskQueue，从任务队列中取任务
    存储获取的页面源码需要数据队列，dataQueue
    :return:
    """

    while not taskQueue.empty():
        pagenum = taskQueue.get()
        print('正在爬取'+str(pagenum)+'页',os.getpid())
        fullUrl = 'https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page='+str(pagenum)
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        }
        try:
            response = requests.get(url=fullUrl, headers=headers)
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



def parsePageData(dataQueue):
    print('dasdsad')
    while not dataQueue.empty():
        print('正在解析数据')
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

            # 数据持久化
            with open('caipilist.json','a+') as file:
                json_str = json.dumps(item,ensure_ascii=False) + '\n'
                file.write(json_str)




if __name__ == '__main__':

    #任务队列（存放任务）
    # taskQueue = queue.Queue()
    taskQueue = Queue()
    #https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page=1
    #https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page=2
    #https://www.meishij.net/chufang/diy/jiangchangcaipu/?&page=3
    for page in range(1,57):
        taskQueue.put(page)

    # 数据队列（存放爬取进程获取的页面源码数据）
    # dataQueue = queue.Queue()
    dataQueue = Queue()

    #爬取进程（执行下载任务）
    crawlProcesses = []
    for i in range(1,4):

        crawlProcess = Process(
            target=crawlTaskRequest,
            args=(taskQueue,dataQueue)
        )
        #开启进程执行任务
        crawlProcess.start()

        crawlProcesses.append(crawlProcess)
    # #爬取进程设置阻塞，等待任务队列中的任务爬取完毕,回到主进程中继续执行
    for crawlProcess in crawlProcesses:
        crawlProcess.join(timeout=5)

    print(dataQueue.empty())
    #解析进程（将数据队列中的页面源码数据取出来，解析）
    parseProcesses = []
    for i in range(1,3):

        parseProcess = Process(
            target=parsePageData,
            args=(dataQueue,)
        )
        #开启进程执行任务
        parseProcess.start()
        parseProcesses.append(parseProcess)

    # # 解析线程设置阻塞，等待数据队列中的页面源码解析完毕
    for parseProcess in parseProcesses:
        parseProcess.join()

    print('结束')



