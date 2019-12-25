# 线程池：目的是为了方便快捷的创建线程
# 线程池中的线程不需要手动管理，我们只
# 要需要往线程池中添加任务，线程池会
# 自动分配任务给线程执行，线程执行完毕后
# 我们可以设置回调函数，处理结果

from concurrent.futures import ThreadPoolExecutor
import time,threading
def download_data(url):
    #让线程执行这个请求任务
    print(url,threading.currentThread().name)
    #等带1秒模拟发起请求
    time.sleep(1)

    return 200,'请求成功',url

def download_done(futures):
    """
    想根据返回结果做什么功能，就在这里实现代码
    :param futures:
    :return:
    """
    #使用futures.result()获取回调结果
    code,html,url = futures.result()
    print(code,html,url)

if __name__ == '__main__':

    print('开启',threading.currentThread().name)

    #创建线程池
    #max_workers:设置线程池中的线程数（并不是越大越好）
    pool = ThreadPoolExecutor(10)

    for i in range(1,100):
        #往线程池中提交任务
        url = 'https://www.baidu.com/'+str(i)
        result = pool.submit(download_data,url)
        #add_done_callback()设置回调函数
        result.add_done_callback(download_done)

    #内部实现了t.join()方法
    pool.shutdown()

    print('结束', threading.currentThread().name)





