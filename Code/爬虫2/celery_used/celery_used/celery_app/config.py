# 官方配置文档：查询每个配置项的含义。
# http://docs.celeryproject.org/en/latest/userguide/configuration.html

#broker(消息中间件来接收和发送任务消息)
# BROKER_URL = 'redis://localhost:6379/1'
BROKER_URL = 'redis://118.24.255.219:6379/1'

#backend(存储worker执行的结果)
CELERY_RESULT_BACKEND = 'redis://118.24.255.219:6379/2'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

#设置时间参照，不设置默认使用的UTC时间
CELERY_TIMEZONE = 'Asia/Shanghai'
#指定任务的序列化
CELERY_TASK_SERIALIZER='json'
#指定执行结果的序列化
CELERY_RESULT_SERIALIZER='json'

from datetime import timedelta
from celery.schedules import crontab
#celery 定时任务,分两种
# 固定间隔时间发送任务
# 固定每一天的某个时间发送任务
CELERYBEAT_SChEDULE = {
    'task1_add': {
        'task':'celery_app.tesk1.add',#指定定时发送的任务
        'schedule':timedelta(hours=0,minutes=0,seconds=10),#指定定时发送的时间间隔
        #函数的参数，元组类型
        'args':(40,)
    },
    #固定每天某个时间发送任务
    'task2_add':{
        'task':'celery_app.tesk1.add',
        'schedule':crontab(hour=14,minute=25)
    }
}