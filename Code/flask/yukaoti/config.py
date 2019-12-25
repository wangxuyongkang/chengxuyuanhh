class Config(object):

    DEBUG = True
    # db
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/lolhero'
    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True


class DevConfig(Config):
    DEBUG = True

# 线上配置
class ProConfig(Config):
    DEBUG =  False


configs = {
    'dev':DevConfig,
    'pro':ProConfig
}