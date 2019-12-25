import time
import random
from celery import Celery

# #同步任务执行
# def add(num):
#     print('task enter......')
#     random_obj = random.Random()
#     num1 = random_obj.randint(0,num)
#     num2 = random_obj.randint(0,num)
#     time.sleep(5)
#     print('task end....')
#     return num1+num2
#
# if __name__ == '__main__':
#     sum = add(10)
#     print(sum)

#broker:消息中间件，用来接受任务和发送任务消息
broker = 'redis://127.0.0.1:6379/1'
#backend:结果存储区，用来存放任务执行单元返回的结果
backend = 'redis://127.0.0.1:6379/2'
app = Celery(
    'demo',
    broker=broker,
    backend=backend,
)

# 添加@app.task()装饰器，说明要执行的任务
# 是一个异步任务
@app.task()
def add(num):
    print('task enter......')
    random_obj = random.Random()
    num1 = random_obj.randint(0,num)
    num2 = random_obj.randint(0,num)
    time.sleep(5)
    print('task end....')
    return num1+num2

# if __name__ == '__main__':
#
#     sum = add.delay(20)
#     print(sum)
    # 8c2114db-ac02-4d11-846b-18db4d10bc95,
    # 异步任务的taskid