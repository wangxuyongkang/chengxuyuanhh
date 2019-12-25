from celery import Celery

app = Celery(
    'demo',
    include=[
        'celery_app.tesk1',
    ]
)

##通过配置文件加载配置信息
app.config_from_object(
    'celery_app.config'
)

