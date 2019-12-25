# 1.多线程可以实现多任务
# 2.线程的执行是无序的
# 3.线程是cpu执行的基本单元
# 4.线程是依赖于进程存在的，同一进程下的线程共享进程资源
# 5.线程锁(互斥锁): 为了保证同一时刻只有一个线程再修改资源（注意死锁）
# 6.线程多用来处理I/O密集型任务(文件的读写 网络的请求 （网络I/O）)
# 7.全局解释器锁: 因为python解释器的原因，存在GIF全局解释器锁，保证同一时刻只有一个线程在执行
###在多线程中(list,dict,tuple)都是非线程安全的，需要使用到互斥锁，而我们往往在线程之间实现数据的传递和通讯的时候添加
import threading


def writedata(row):
    for i in range(row):
        print(i)

if __name__ == '__main__':
    '''
    target ： 线程执行的目标函数
    name   线程名称
    args执行函数需要的参数
    kwargs执行函数需要的参数
    '''
    thread = threading.Thread(target=writedata(10),
                              name='write'
                              )

    #daemon=True 主线程结束，子进程随着结束
    #daemon=Flase（默认）：主线程结束，子进程继续执行
    thread.daemon = True
    #开启线程
    thread.start()
    #join 线程阻塞
    thread.join()