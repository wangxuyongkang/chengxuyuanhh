### 线程池:在执行多线程任务的时候，我们只需要告诉线程池，需要创建的线程数量，以及线程要执行的函数，其他线程的管理  不用开发者控制

from concurrent.futures import ThreadPoolExecutor #线程池
import threading,time,requests

def task(url):
    time.sleep(1)
    print(url,threading.current_thread().name)
    ##执行下载
    response = requests.get(url)
    return response

def parse_data(future):
    '''这个方法统一解析数据'''
    #future.result()获取返回值
    response = future.result()
    print(response.status_code)
if __name__ == '__main__':
    print('开启',threading.current_thread().name)
    #实例化线程池
    #max_workers:指定线程数量
    pool = ThreadPoolExecutor(10)
    for i in range(0,100):
        url = 'https://www/baidu.com/?p='+str(i)
        result = pool.submit(task,url)
        # 给线程池中执行的任务，添加回调函数
        result.add_done_callback(parse_data)
    #内部实现了join方法
    pool.shutdown(wait=True)
    print('结束', threading.current_thread().name)