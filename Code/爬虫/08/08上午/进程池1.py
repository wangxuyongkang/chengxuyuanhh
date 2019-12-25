# 进程池两种创建方式
from multiprocessing import Pool
import requests
def download_data(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    }
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        return response.status_code,response.url

#进程任务执行完后的回调函数
def download_done(result):
    print(result)


if __name__ == '__main__':

    #创建进程池
    #可以设置进程池中的进程数量
    processPool = Pool(4)

    for i in range(1,200):
        #提交任务
        # processPool.apply() #同步的方式提交任务，效率慢
        # processPool.apply_async() #异步的方式提交任务，效率高
        url = 'https://www.baidu.com/'+str(i)
        processPool.apply_async(
            download_data,args=(url,),callback=download_done
        )

    #调用close后就不能在往进程池中添加任务了
    processPool.close()
    processPool.join()



