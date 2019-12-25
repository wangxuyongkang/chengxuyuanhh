from flask import Flask,render_template,request,redirect,url_for,abort
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
manager = Manager(app)
# 设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/1809_flask'

# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 数据库和模型类同步修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# 创建数据库迁移对象
Migrate(app, db)

# 向脚步管理添加数据库迁移命令 db指命令的别名
manager.add_command('db', MigrateCommand)
class type(db.Model):
    __tablename__ = 'tbl_types'
    # 数据库真正存在的字段
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(64),default='')
    type_l = db.Column(db.String(32),unique=True)  # 类型
    heros = db.relationship("game", backref='type')
    def __str__(self):
        return self.title


class game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(32),default='')  # 标题
    describe = db.Column(db.String(64),default='') # 描述
    # 外键关联
    type_id = db.Column(db.Integer, db.ForeignKey("tbl_types.id"))
    def __repr__(self):
        return self.title


@app.route('/')
def index():
    games = game.query.all()
    if games:
        cxt={
            'games':games
        }
        return render_template('describe_1.html',**cxt)
    else:
        return abort(404)

@app.route('/list')
def list():
    types = type.query.all()
    if types:
        cxt= {
            'types':types
        }
        return render_template('list.html',**cxt)
    else:
        return abort(404)



if __name__ == '__main__':
    manager.run()