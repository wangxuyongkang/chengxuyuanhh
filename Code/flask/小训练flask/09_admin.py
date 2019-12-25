from flask import Flask,current_app,redirect,url_for,request
from flask_admin import Admin

from flask_admin.contrib.sqla import ModelView
from .modelview import BaseModelview
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import pymysql
from datetime import datetime

pymysql.install_as_MySQLdb()
app = Flask(__name__)
manager = Manager(app)
db = SQLAlchemy(app)
Migrate(app, db)
app = Flask(__name__)
admin = Admin(app=app,name='后台管理',template_mode='bootstrap3')
admin.add_view(BaseModelview(User, db.session,name=u'用户管理'))
admin.add_view(BaseModelview(Tag, db.session, name=u'标签管理'))
admin.add_view(BaseModelview(Article, db.session, name=u'文章管理'))


manager.add_command('db', MigrateCommand)

# 设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/1809_flask_1'
# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 数据库和模型类同步修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(32))
    content=db.Column(db.Text,nullable=False)
    tag=db.Column(db.String(64),nullable=True)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.title

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    desc = db.Column(db.String(64), nullable=True)
    create_time = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.name
if __name__ == '__main__':
    manager.run()