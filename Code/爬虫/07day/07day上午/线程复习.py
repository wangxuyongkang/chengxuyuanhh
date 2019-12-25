#使用线程
import threading
import time

sum = 0

def work_one(num):
    global sum
    print(num)
    lockA.acquire() #枷锁
    time.sleep(1)
    lockB.acquire()
    for i in range(0,num):
        # time.sleep(0.05)
        #threading.currentThread().name获取线程的名称
        # print(threading.currentThread().name,i)
        sum += 1
    lockA.release() #解锁

def work_two(num):

    print(num)
    global sum
    lockB.acquire()  # 枷锁
    time.sleep(1)
    lockA.acquire()
    for i in range(0,num):
        # time.sleep(0.05)
        #threading.currentThread().name获取线程的名称
        # print(threading.currentThread().name,i)
        sum += 1
    lockB.release()  # 解锁

def work_three(num):

    print(num)
    global sum
    # lock.acquire()  # 枷锁
    for i in range(0,num):
        # time.sleep(0.05)
        #threading.currentThread().name获取线程的名称
        # print(threading.currentThread().name,i)
        sum += 1
    # lock.release()  # 解锁

if __name__ == '__main__':

    #创建线程
    """
    target:线程要执行的目标函数
    name：给线程起一个名称
    args:传参数（元组）
    kwargs:传参数（字典）
    """
    print('开启',threading.currentThread().name)

    # 创建线程锁：
    # 保护资源，添加了线程锁之后，同一时刻只能有一个线程在修改资源
    # 注意死锁情况
    lockA = threading.Lock()
    lockB = threading.Lock()

    thread_one = threading.Thread(
        target=work_one,name='Thread_workone',
        args=(1000000,)
    )
    thread_two = threading.Thread(
        target=work_two, name='Thread_worktwo',
        args=(1000000,)
    )
    # thread_three = threading.Thread(
    #     target=work_three, name='Thread_workthree',
    #     args=(1000000,)
    # )

    # 前台线程和后台线程
    #default to daemon = False(后台线程,主线程结束不影响子线程运行)
    # default to daemon = False(前台线程,主线程子线程随之结束)
    # thread_one.daemon = True
    # thread_two.daemon = True
    # thread_three.daemon = True

    #开启线程
    thread_one.start()
    thread_two.start()
    # thread_three.start()
    #线程的执行是无顺序的

    # #线程阻塞（join让自线程中的任务执行完毕后，再回到主线程
    # # 中继续执行）
    thread_one.join()
    thread_two.join()
    # thread_three.join()

    # time.sleep(2)
    print(sum)
    print('结束', threading.currentThread().name)