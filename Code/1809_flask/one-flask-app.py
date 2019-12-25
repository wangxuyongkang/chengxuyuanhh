from flask import Flask,redirect,url_for


#创建对象
#__name__代表当前
#static_url_path隐藏真实路径
app = Flask(__name__,static_url_path='/1809')

#路由和视图
@app.route('/')#代表首页
def index():
    # name = app.config.get('gebi')
    return '首页'

# @app.route('/center')
# def center():
#     return redirect(url_for('login'))#重定向方法


#重定向
@app.route('/login',methods=['GET','POST'])#请求方式
def login():
    return 'login'



'''

转换器
int string float 不写默认为string    path

'''
#匹配数字
@app.route('/center/<int:uid>')
def center(uid):
    return 'your uid is {0}'.format(uid)
#字符串匹配
@app.route('/center1/<string:uid>')
def center1(uid):
    return 'your uid is {0}'.format(uid)
#浮点类型匹配
@app.route('/center2/<float:uid>')
def center2(uid):
    return 'your uid is {0}'.format(uid)
#类型
@app.route('/center3/<uid>/')
def center3(uid):
    return 'your uid is {0}'.format(uid)
#转换器的本质就是正则
@app.route('/center4/<path:uid>')
def center4(uid):
    return 'your uid is {0}'.format(uid)

#请求方法 get post delete put options



#文件形式 -----把配置文件加载到app对象中
#app.config.from_pyfile('config.cfg')
#类形式----
#class Config():
#    DEBUG = True

from werkzeug.routing import BaseConverter,FloatConverter#基类


#转换器重写 让匹配规则 能写活
class myConverter(BaseConverter):

    def __init__(self,map,re):
        super().__init__(map)
        self.regex = re

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
#注册转换器
app.url_map.converters['mc'] = myConverter

@app.route('/center5/<mc(r"\d{5,10}"):uid>')#匹配规则
def center5(uid):
    print(type(uid))
    return 'your uid is {0}'.format(uid)


#手机匹配规则
@app.route('/center6/<mc(r"1[3456789]\d{9}"):uid>')
def enter6(uid):
    print(type(uid))
    return redirect(url_for('center5',uid='123456'))



#app.config.from_object(Config)

#直接操作app.config 适用于参数少的情况下

#app.config['DEBUG'] = True

#自定义参数
# app.config['gebi'] = 'laowang'

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000',debug=True)