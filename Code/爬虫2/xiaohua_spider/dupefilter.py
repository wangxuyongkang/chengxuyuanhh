import redis
import hashlib


# TODO: Rename class to RedisDupeFilter.
class RFPDupeFilter(object):

    def __init__(self, server=None, key='request:fingerprint'):
        # redis数据库链接
        self.server = server
        if not self.server:
            self.server = redis.StrictRedis(
                host='118.24.255.219',
                port=6380,
                db=0,
            )
        # 指定指纹要存在哪个key下
        self.key = key

    def request_seen(self, url):
        ###传递url，判断url是否请求过
        fp = self.request_fingerprint(url)

        # This returns the number of values added, zero if already exists.
        # sadd使用这个方法往redis数据库的指纹集合(set)中添加指纹
        # 指纹能添加成功，返回1, 表示url地址未请求过;
        # 指纹添加不成功，返回0，表示url地址请求过;
        added = self.server.sadd(self.key, fp)
        return added

    def request_fingerprint(self, url):
        # 生成指纹，使用的md5加密生成指纹
        """生成指纹"""
        md5_obj = hashlib.md5()
        md5_obj.update(url.encode('utf-8'))
        return md5_obj.hexdigest()