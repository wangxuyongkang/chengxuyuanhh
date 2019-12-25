class Config(object):
    SECRET_KEY = 'SAJKDHSJAKDH'

    DEBUG = True
    # db
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/09waimai'
    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    APP_ID = 'wx07d17730be1f4d3e'
    APP_SECRET = 'bddd1135988e53717e9fee57f732b919'
    DOMAIN = 'http://127.0.0.1:5000'
    IGNORE_URLS = ['/api/v1/user/login','/api/v1/user/cklogin','/api/v1/food/all','/api/v1/food/search','/api/v1/food/info']
class DevConfig(Config):
    DEBUG = True

# 线上配置
class ProConfig(Config):
    DEBUG =  False




configs = {
    'dev':DevConfig,
    'pro':ProConfig
}