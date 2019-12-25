import random,time
from celery_used.celery_used.celery_app import app

@app.task()
def add(num):
    print('task enter......')
    random_obj = random.Random()
    num1 = random_obj.randint(0,num)
    num2 = random_obj.randint(0,num)
    time.sleep(5)
    print('task end....')
    return num1+num2

