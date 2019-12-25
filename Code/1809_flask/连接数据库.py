from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
# 设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/1809_flask'

# 数据库和模型类同步修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class gameType(db.Model):
    __tablename__ = 'tbl__game__type'#表名
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),nullable=False,unique=True)
    #不存在数据库当中，只是方便查找
    heros = db.relationship('gameHero',backref='type')
    def __str__(self):
        return self.name

class gameHero(db.Model):
    __tablename__ = 'tbl__game__hero'  # 表名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    gender = db.Column(db.SmallInteger,default=1)
    type_id = db.Column(db.Integer,db.ForeignKey('tbl__game__type.id'))
    @property
    def sex(self):
        return '男' if self.gender == 1 else '女'
@app.route('/')
def index():
    #查询所有英雄
    gameheros = gameHero.query.all()

    #查询所有类别
    gametypes = gameType.query.all()
    # 根据性别查找
    g_heros = gameHero.query.filter_by(gender=0).all()

    # g_heros = gameHero.query.filter(gameHero.gender == 0).all()

    # 根据性别和类型查询
    d_heros = gameHero.query.filter_by(gender=0, type_id=2).all()

    # 类型为射手或性别为男的英雄
    f_heros = gameHero.query.filter(or_(gameHero.type_id == 1, gameHero.gender == 1))

    ctx = {
        'gameheros':gameheros,
        'gametypes':gametypes,
        'g_heros':g_heros,
        'd_heros' :d_heros,
        'f_heros':f_heros
    }
    return render_template('cha.html',**ctx)
@app.route('/show/<id>',methods=['GET','POST'])
def show(id):
    if request.method == 'GET':
        heros = gameHero.query.get(id)
        cxt = {
            'heros':heros,
        }
        return render_template('show.html',**cxt)
    else:
        new_name = request.values.get('new_name')
        new_gender = request.values.get('new_gender')
        gameHero.query.filter_by(id=id).update({'name':new_name,'gender':new_gender})
        db.session.commit()
        return redirect(url_for('index'))
        # return "{}--{}".format(new_name,new_gender)
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'GET':
        types = gameType.query.all()
        cxt = {
            'types' : types
        }
        return render_template('add.html',**cxt)
    else:
        new_name = request.values.get('new_name')
        new_gender = request.values.get('new_gender')
        types_one = request.values.get('type_id')
        db.session.add(gameHero(name=new_name,gender=new_gender,type_id=types_one))
        #gameHero.query.filter_by(id=id).add({'name': new_name, 'gender': new_gender,'type_id':types_one})
        db.session.commit()
        return redirect(url_for('index'))
if __name__ == '__main__':
     app.run(debug=True)
    # db.drop_all()#删除表
    # db.create_all()#创建表
    #
    # gt = ganeType(name='射手')
    # db.session.add(gt)#把对象加入到会话里面
    # db.session.commit()  # 提交
    #
    # gt1 = ganeType(name='法师')
    # db.session.add(gt1)#把对象加入到会话里面
    # db.session.commit()  # 提交
    #
    # gh = gameHero(name='后裔',gender=1,type_id=gt.id)
    # gh1 = gameHero(name='鲁班',gender=1,type_id=gt.id)
    # gh2 = gameHero(name='孙尚香',gender=0,type_id=gt.id)
    # gh3 = gameHero(name='李元芳',gender=1,type_id=gt.id)
    #
    # gh4 = gameHero(name='甄姬',gender=0,type_id=gt1.id)
    # gh5 = gameHero(name='诸葛亮',gender=1,type_id=gt1.id)
    # gh6 = gameHero(name='周瑜',gender=1,type_id=gt1.id)
    # gh7 = gameHero(name='大乔',gender=0,type_id=gt1.id)
    # db.session.add_all([gh,gh1,gh2,gh3,gh4,gh5,gh6,gh7])
    # db.session.commit()#提交



