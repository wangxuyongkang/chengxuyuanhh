#multiprocessing跨平台的库，可以实现多进程

# 进程的执行是无序的
# 进程是系统分配资源的基本单元,每一个进程都有自己
# 独立的内存空间，进程之间的资源是不共享的
# 进程之间的通讯
# 进程是包含线程的
# 进程多用来处理计算密集型任务


from multiprocessing import Process,Queue
import os

data = []

def task(row,**kwargs):
    print('子进程id',os.getpid(),'父id',os.getppid())
    print(row,kwargs)
    # global data
    for i in range(row):
        my_queue.put(i)
        # data.append(i)

def task2(row,**kwargs):
    # print('子进程id',os.getpid(),'父id',os.getppid())
    # print(row,kwargs)
    # global data
    # for i in range(row):
    #     data.append(i)
    #
    # print(data)
    # global data
    # print(len(data))

    while not my_queue.empty():
        print(my_queue.get())

    print(my_queue.empty())


if __name__ == '__main__':

    #创建进程
    """
    target: Optional[Callable] = ...,
    name: Optional[str] = ...,
    args: Iterable[Any] = ...,
    kwargs: Mapping[Any, Any] = ...,
    """
    my_queue = Queue()

    print('主进程开启主进程id',os.getpid())
    process1 = Process(
        target=task,
        args=(10,),
        kwargs={'name':'进程一号'}
    )
    #启动进程
    process1.start()

    #进程阻塞
    process1.join()

    process2 = Process(
        target=task2,
        args=(10,),
        kwargs={'name': '进程二号'}
    )
    # 启动进程
    process2.start()

    # 进程阻塞
    process2.join()

    print('主进程结束主进程id', os.getpid())