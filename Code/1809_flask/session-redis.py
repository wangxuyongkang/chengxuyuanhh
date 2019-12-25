from flask import Flask,request,session
import redis
from flask_session import Session

f_session = Session()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'laowangaigebi'#加密的密钥
app.config['SESSION_USE_SIGNER'] = True#是否对发送到浏览器上的session的cookie值进行加密
app.config['SESSION_TYPE'] = 'redis'#session类型为redis
app.config['SESSION_KEY_PREFIX'] = 'session:'#保存到session中的值的前缀
app.config['PERMANENT_SESSION_LIFETIME'] = 7200#失效时间
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',port='6379',db=4)#连接redis数据库

#绑定flask的对象
f_session.init_app(app)

@app.route('/')
def index():
    session['xingming'] = 'laozhao'
    return '存在session'

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)