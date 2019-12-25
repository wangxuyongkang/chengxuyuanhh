# 使用进程可以充分了用cpu资源，是cpu分配资源的基本单元
# 每一个进程都有自己的内存空间，同样是无须执行，进程之间
# 资源不共享，多用进程处理计算密集型任务，进程可以实现并
# 行的操作

# 并发：同时发起，但是不是同时执行，交替执行
# 并行：同时发起，同时执行

#multiprocessing并不是python自带的,是跨平台一个库，
#只是集成进来，提供给我们使用
from multiprocessing import Process,Queue
import os

# data_list = []

def add_data(num,data_queue,**kwargs):
    print(num,kwargs)
    # global data_list

    for i in range(0,num):
        # data_list.append(i)
        data_queue.put(i)
        print('添加：',os.getpid(),os.getppid())

def read_data(dataqueue):
    while not dataqueue.empty():
        print('取出来了',dataqueue.get())
        print('读取：', os.getpid(), os.getppid())

if __name__ == '__main__':


    #使用multiprocessing 的Queue实现数据的共享（传递）
    #maxsize设置队列中能够存放元素的最大数量
    data_queue = Queue()

    #创建进程
    """
    target: Optional[Callable] = ...,(进程执行的函数)
    name: Optional[str] = ...,（进程名称）
    args: Iterable[Any] = ...,（传参数）
    kwargs: Mapping[Any, Any] = ...,（传参数）
                 *,
    daemon: Optional[bool] = ...) ->（设置前后太进程）
    """
    process1 = Process(
        target=add_data,args=(100,data_queue),kwargs={'name':'进程1号'}
    )

    #执行
    process1.start()

    #join设置进程阻塞，确保子进程中的任务执行完，然后回到住进程执行
    process1.join(timeout=10)

    # print(data_list)
    #empty()判断队列是否为空（Flase：不为空，True：为空）
    print(data_queue.empty())

    process2 = Process(target=read_data,args=(data_queue,))

    process2.start()

    process2.join()

    print('111111')



