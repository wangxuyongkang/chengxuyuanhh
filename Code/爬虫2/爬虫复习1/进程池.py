from concurrent.futures import ProcessPoolExecutor
# import requests
#
# def task(url):
#     headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3738.400'
#     }
#     response = requests.get(url,headers)
#     if response.status_code == 200:
#         return response.text,response.status_code
#
# def done_task(future):
#     text,code = future.result()
#     print(len(text),code)
#
# if __name__ == '__main__':
#     process_pool = ProcessPoolExecutor(8)
#     for i in range(100):
#         url = 'htttps://www.baidu.com/?p='+str(i)
#         #往进程池中添加执行函数,和执行函数相关参数
#         result = process_pool.submit(task,url)
#         #添加回调函数
#         result.add_done_callback(done_task)
#     #阻塞
#     process_pool.shutdown()
#     print('任务都执行完毕了')

###########################################方法二
import requests
from multiprocessing import Pool
def task(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3722.400 QQBrowser/10.5.3738.400'
    }
    response = requests.get(url,headers)
    if response.status_code == 200:
        #返回参数future接收
        return response.text,response.status_code

def done_task(future):
    #future：执行函数返回什么，就接收什么
    print(future)


if __name__ == '__main__':
    #创建进程池
    process_pool = Pool(8)
    for i in range(1,101):
        url = 'htttps://www.baidu.com/?p='+str(i)
        #apply_async异步方式添加执行任务

        process_pool.apply_async(task,args=(url),callback=done_task)
        #apply可以同步的方式添加任务
        # process_pool.apply()

        #close关闭进程池
        process_pool.close()

        #阻塞
        process_pool.join()
        print('全部任务执行完毕')