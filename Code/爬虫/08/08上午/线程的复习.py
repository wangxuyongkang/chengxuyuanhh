#线程是为了实现多任务

# 线程是依赖于进程存在的，并且一个进程下，可以有多个线程
# 线程共享进程的资源，在python中多线程是并发进行的，GIL
# (全局解释器锁)，所以同一时刻只有一个线程被执行。线程多
# 用于处理I/O密集型操作（文件读写操作，网络I/O）

#线程执行是无序的
#线程之间的资源是共享的
#线程锁的作用:确保同一时刻只有一个线程在访问资源
   #注意：死锁的情况

import threading

# data_list = []
sum = 0
def add_data(num,**kwargs):
    # global data_list
    global sum
    lock.acquire() #加锁
    for i in range(0,num):
        # data_list.append(i)
        sum += 1
    lock.release() #解锁


if __name__ == '__main__':

    """
    target=None, 设置线程要执行的目标函数
    name=None, 线程名称
    args=(), 目标函数需要的参数
    kwargs=None,目标函数需要的参数
    daemon=None，（设置前台和后台线程）
    """

    lock = threading.Lock()

    thread1 = threading.Thread(
        target=add_data,
        args=(100000,),
        kwargs={'name':'张三'},
        name= '蚕蛾一号'
    )

    #开启线程
    thread1.start()

    #线程阻塞（确保自线程中的任务执行完毕，然后回主线程中继续执行）
    #timeout=10 设置阻塞的时间
    # thread1.join(timeout=10)

    thread2 = threading.Thread(
        target=add_data,
        args=(100000,),
        kwargs={'name': '张三'},
        name='蚕蛾一号'
    )

    # 开启线程
    thread2.start()

    # 线程阻塞（确保自线程中的任务执行完毕，然后回主线程中继续执行）
    # timeout=10 设置阻塞的时间
    thread1.join(timeout=10)
    thread2.join(timeout=10)

    print(sum)


