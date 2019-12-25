# from tasks import add
#
# if __name__ == '__main__':
#
#     result = add.delay(10)
#     print(result)

from celery_app import tesk1

if __name__ == '__main__':

    tesk1.add.delay(30)