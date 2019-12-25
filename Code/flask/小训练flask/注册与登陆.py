from flask import Flask, render_template, request,session,redirect,url_for
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import pymysql
import redis
from flask_session import Session
from datetime import datetime
pymysql.install_as_MySQLdb()

app = Flask(__name__)
manager = Manager(app)
db = SQLAlchemy(app)
Migrate(app, db)

# 初始化Session对象
f_session = Session()
app.config['SECRET_KEY'] = 'laowangaigebi'  # 加密的密钥
app.config['SESSION_USE_SIGNER'] = True  # 是否对发送到浏览器上session的cookie值进行加密
app.config['SESSION_TYPE'] = 'redis'  # session类型为redis
app.config['SESSION_KEY_PREFIX'] = 'session:'  # 保存到session中的值的前缀
app.config['SESSION.PERMANENT'] = True  # 失效时间 秒
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port='6379', db=4)  # redis数据库连接
# session.permanent=True
# 绑定flask的对象
f_session.init_app(app)




manager.add_command('db', MigrateCommand)
# 设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/1809_flask_1'

# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 数据库和模型类同步修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True


class Users(db.Model):
    __tbluser__ = 'tbl_user——info'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), default='')
    password = db.Column(db.String(128), default='')
    nickname = db.Column(db.String(32), default='')
    gender = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DATETIME, default=datetime.now())
    update_time = db.Column(db.DATETIME, default=datetime.now(),onupdate=True)

    @property
    def sex(self):
        return '男' if self.gender == 1 else '女'

import re
def re_phone(phone):
    return re.match(r'1[3456789]\d{9}',phone)
#加密
import hashlib
def spwd(pwd):
    md5 = hashlib.md5
    md5.update(pwd.endcode('utf-8'))
    return md5.hexdigest()


@app.route('/index')
@app.route('/')
def index():
    uid =session.get('uid')
    if not uid:
        return render_template('index.html')
    user = Users.query.get(uid)
    if not user:
        return render_template('index.html')
    users = Users.query.filter(Users.gender != user.gender).all()
    ctx = {
        'users',users,
        'user',user
    }
    return render_template('index.html',**ctx)
@app.route('/register', methods=['GET', 'POST'])
def register():
    # return render_template('register.html')
    # User = request.values.all()
    if request.method == "GET":
        return render_template('register.html')
    else:
        phone = request.values.get('phone')
        password = request.values.get('password')
        password1 = request.values.get('password1')
        nickname = request.values.get('nickname')
        gender = request.values.get("gender")
        if not all([phone,password1,password,nickname,gender]):
            return render_template('register.html')
        if len(phone) != 11 or not re_phone(phone):
            return render_template('register.html')
        if len(password) < 6 or len(password) > 16:
            return render_template('register.html')
        if password != password1:
            return render_template('register.html')
        if len(nickname) < 6 or len(nickname) >16:
            return render_template('register.html')
        if gender not in ['0','1']:
            return render_template('register.html')
        user = Users.query.filter_by(phone = phone).first()
        if user:
            return render_template('register.html')
        userinfo = Users()
        userinfo.phone = phone
        userinfo.password = spwd(password)
        userinfo.nickname = nickname
        userinfo.gender = gender
        db.session.add(userinfo)
        db.session.commit()
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    phone = request.values.get('phone')
    password = request.values.get('password')
    user = Users.query.filter_by(phone=phone).first()
    if not user:
        return redirect(url_for('register'))
    if user.password != spwd(password):
        return render_template('login.html')
    #状态保持
    session['uid'] = user.id
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    manager.run()
