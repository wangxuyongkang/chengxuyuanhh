from flask import Flask,render_template
from jinja2.filters import do_int


app = Flask(__name__)

#路由和视图
@app.route('/index')
@app.route('/')#代表首页
def index():
    ctx = {
        'name' : 'laowang',
        'age':17,
        'hobby':["下棋","看电影","吃饭"],
        'test':{"a":1,"b":2},
        'center':'<em>hello</em>',
        'password':'123456'

    }
    return render_template('index.html',**ctx)


#自定义过滤器
import hashlib
def do_password(s):
    md5 = hashlib.md5()
    md5.update(s.encode('utf8'))
    return md5.hexdigest()
#注册
#自定义过滤器
def do_add(s,code = 1):
    s = int(s)+code
    return str(s)
app.jinja_env.filters['add'] = do_add
app.jinja_env.filters['dp'] = do_password



if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000',debug=True)