import redis,json

#redis数据库链接
redis_cli = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    #数据库的索引值
    db=2,
)

while True:
    #获取所有的key
    keys = redis_cli.keys()
    # print(keys)
    for key in keys:
        # print(key)
        key = key.decode('utf-8')
        data = redis_cli.get(key)
        try:
            result = json.loads(data)
            print(result)
            redis_cli.delete(key)
        except Exception as err:
            print(err)


