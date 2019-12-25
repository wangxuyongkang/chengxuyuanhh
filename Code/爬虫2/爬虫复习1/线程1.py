# 1.多线程可以实现多任务
# 2.线程的执行是无序的
# 3.线程是CPU执行的基本单元
# 4.线程是依赖于进程存在的,同一进程下的线程共享进程的资源
# 5.线程锁（互斥锁）: 为了保证同一时刻只有一个的线程在修改资源，
# （注意死锁问题）
# 6.线程多用来处理I/O密集型任务（文件读写、网络请求（网络I/O））
# 7.全局解释器锁: 因为python解释器的原因，存在GIL全局解释器锁，
#             保证同一时刻只有一个线程在执行（深入了解）

### 在多线程中（list、tuple、dict）都是非线程安全的,需要使用
# 到互斥锁，而我们往往在线程之间实现数据的传递和通讯的时候，会用
# 到queue队列，队列是线程安全的

import threading,time
import queue

data = []

def writedata(row):
    time.sleep(1)
    # global data
    print(threading.currentThread().name)
    # lock.acquire() #枷锁
    for i in range(row):
        # data.append(i)
        #put():往队列中存放数据
        my_queue.put(i)
    # lock.release() #解锁

def readdata():
    #empty():判断队列是否为空

    #empty(): 队列为空返回True,队列不为空返回Flase
    while not my_queue.empty():
        #get()取值
        print(my_queue.get())

# def writedataA(row):
#     global data
#     print(threading.currentThread().name)
#     lockA.acquire() #枷锁
#     time.sleep(1)
#     lockB.acquire()
#     for i in range(row):
#         data.append(i)
#     lockA.release()
#
#
# def writedataB(row):
#     global data
#     print(threading.currentThread().name)
#     lockB.acquire() #枷锁
#     time.sleep(1)
#     lockA.acquire()
#     for i in range(row):
#         data.append(i)
#     lockB.release() #解锁


if __name__ == '__main__':

    #创建队列
    #maxsize:设置队列的最大容量
    #队列读取数据:(FIFO)
    my_queue = queue.Queue()

    #互斥锁
    lock = threading.Lock()

    # ##死锁现象
    # lockA = threading.Lock()
    # lockB = threading.Lock()

    print('开启:',threading.currentThread().name)
    #target:线程要执行的目标函数, name：线程的名称,
    #args=():执行函数需要的参数, kwargs=None:执行函数需要的参数
    thread1 = threading.Thread(
        target=writedata,args=(10,),
        name='writethread1'
    )
    #daemon=True:主线程结束，子线程随着结束
    #daemon=Flase（默认）：主线程结束，子线程继续执行
    # thread1.daemon = True

    # thread2 = threading.Thread(
    #     target=writedataA, args=(10,),
    #     name='writethread2'
    # )
    #
    # thread3 = threading.Thread(
    #     target=writedataB, args=(10,),
    #     name='writethread3'
    # )

    thread4 = threading.Thread(
        target=readdata,
        name='writethread4'
    )

    #开启线程
    thread1.start()
    # join()线程阻塞
    thread1.join()

    # thread2.start()
    # thread2.join()

    # thread3.start()

    thread4.start()
    thread4.join()
    # thread2.join()
    # thread3.join()

    print('结束:', threading.currentThread().name)
    print(data)


