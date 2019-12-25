from celery import Celery

app =Celery(
    'xiaohua',
    include=[
        'xiaohua_spider.spider'
    ]
)
app.config_from_object(
    'xiaohua_spider.config'
)