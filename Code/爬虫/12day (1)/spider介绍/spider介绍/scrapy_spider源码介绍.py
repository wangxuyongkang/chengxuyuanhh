

#需要记住的属性参数
# name 属性，必须存在，表示爬虫的名称
# custom_settings (dict）:根据爬虫文件，
# 自定义参数，可以覆盖settings.py文件中的全局参数
#crawler: 是一个对象，包含了爬虫的各个核心组件，其中
#常用的是settings
#settings :指的是settings.py 文件

# def start_requests(self):
#     根据start_urls构建Request对象，发起请求
#     方法内部调用的就是make_requests_from_url()

# def make_requests_from_url():
#     根据url地址构建Request对象

#def parse(self, response):
#     请求成功后的回调方法（必须要实现的方法）

#def update_settings(cls, settings):
#    根据custom_settings中自定义的参数
#    覆盖settings.py中的参数

# def close(spider, reason):
#    根据信号量，监控爬虫关闭的回调方法



