from flask import request,url_for,render_template,redirect,Flask,session,abort,make_response
from flask_migrate import MigrateCommand,Manager,Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
import pymysql
import redis
import re

pymysql.install_as_MySQLdb()
app=Flask(__name__)
manager=Manager(app)

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


# 设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/db_xiangqin'
# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 数据库和模型类同步修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# 创建数据库迁移对象
Migrate(app,db)
# 向脚步管理添加数据库迁移命令 db指命令的别名
manager.add_command('db', MigrateCommand)

# 辅助表
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
# 用户表
class UserInfo(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(8))
    account = db.Column(db.String(64))
    password = db.Column(db.String(64))
    content = db.Column(db.TEXT)
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
                                 backref=db.backref('followed', lazy='joined'),
                                 lazy='dynamic',
                                cascade='all, delete-orphan')

    def __repr__(self):
        return self.name
#     首页
@app.route('/')
@app.route('/index',methods=['GET'])
def index():
    session_id = request.cookies.get('session')
    print(session_id)
    # print('ooooooooooooooooooooooooooooooooo')
    if session_id == None:
        cxt ={
            'art':'登陆',
            'artl':'login'
        }
        return render_template('index.html',**cxt)
    else:
        name = request.values.get('name')
        gender = request.values.get('gender')
        content = request.values.get('content')
        if gender=='0':
            igender = "女"
            obj = UserInfo.query.filter_by(gender='1')
            sex = "男"
        else:
            igender = "男"
            obj = UserInfo.query.filter_by(gender='0')
            sex = "女"
        ctx = {
            "art": '注销',
            "obj": obj,
            "sex": sex,
            "artl": "Off",
            "name": name,
            "content": content,
            "gender":igender
        }
        return render_template('index.html', **ctx)


# 注销
@app.route('/off')
def off():
    session.clear()
    return redirect(url_for('index'))


# 登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        account = request.values.get('account')
        password = request.values.get('password')
        user = UserInfo.query.all()
        for i in user:
            print(i.account)
            if i.account==account and password==password:
                session['user'] = i.name
                session['gender'] = i.gender
                session['content'] = i.content
                return redirect(url_for('index'))

        else:
            return redirect(url_for('login'))
# 注册
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method=='POST':
        name = request.values.get('name')
        account = request.values.get('account')
        pat = re.compile("^1[35678]\d{9}$")
        pat = bool(re.match(pat,account))
        if pat == False:
            account = None
        # account = re.match(r"^1[35678]\d{9}$", str(account))
        password = request.values.get('password')
        gender = request.values.get('gender')
        content = request.values.get('content')
        print('00000000000000{0}000000{1}0000{2}00{3}000{4}'.format(account,name,password,gender,content))
        if not all([name,account,password,gender]):
            return render_template('register.html')
        else:
            user = UserInfo()
            user1 = UserInfo()
            user.name=name
            user.account=account
            user.password=password
            user.gender=gender
            user.content=content
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    else:
        abort(400)






if __name__ == '__main__':

    manager.run()