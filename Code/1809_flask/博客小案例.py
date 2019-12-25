from flask import Flask, render_template, request, abort
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import pymysql
from datetime import datetime

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


class BaseModel(object):
    create_time = db.Column(db.DATETIME, default=datetime.now())
    update_time = db.Column(db.DATETIME, default=datetime.now(), onupdate=True)


# 辅助表
tbl_tags = db.Table('tbl_tags',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tbl_tag.id')),
                    db.Column('article_id', db.Integer, db.ForeignKey('tbl_article.id'))
                    )


# 文章表
class Article(BaseModel, db.Model):
    __tablename__ = 'tbl_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), default='')
    desc = db.Column(db.String(100), default='')
    content = db.Column(db.Text, default='')
    categroy_id = db.Column(db.Integer, db.ForeignKey('tbl_category.id'))
    categroy = db.relationship('Category', backref='articles')
    tags = db.relationship('Tag', secondary=tbl_tags, backref='articles')


# 分类表

class Category(BaseModel, db.Model):
    __tablename__ = 'tbl_category'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(32), default='')

    # 反向查找
    # articles = db.relationship('Article',breakref='categorys')
    def __repr__(self):
        return self.name


# 标签
# 1个标签 ---->多个文章
# 1篇文章 --->多个标签
# 标签模型
class Tag(db.Model):
    # 表名
    __tablename__ = 'tbl_tag'

    # 数据库真正存在的字段
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(32), unique=True)  # 名字


@app.route('/')
def index():
    category = request.args.get('category')
    tags_id = request.args.get('tag')
    print(tags_id, '---------------------')

    articles = None
    if not category and not tags_id:
        articles = Article.query.order_by(Article.create_time.desc()).all()
    else:
        articles = Article.query.filter_by(categroy_id=category).order_by(Article.create_time.desc()).all()
        # tbl_tag = Tag.query.filter_by(tbl_tags=tags_id).all()

    ctx = {
        'articles': articles,
        # 'tbl_tag': tbl_tag,
    }
    return render_template('list.html', **ctx)


@app.route('/show/<id>')
def show(id):
    article = Article.query.get(id)
    if not article:
        abort(404)
    ctx = {
        'article': article
    }
    return render_template('describe_1.html', **ctx)


if __name__ == '__main__':
    manager.run()
    # # db.drop_all()
    # category = Category()
    # category.name = '科技'
    # category1 = Category()
    # category1.name = '游戏'
    # db.session.add(category)
    # db.session.add(category1)
    # db.session.commit()
    #
    # article = Article()
    # article.title = '华为cpu量产'
    # article.desc = '华为真好'
    # article.content = '华为真好华为真好华为真好华为真好华为真好华为真好华为真好华为真好'
    # article.categroy_id = category.id
    #
    # article1 = Article()
    # article1.title = '王者荣耀'
    # article1.desc = '王者真好'
    # article1.content = '王者真好王者真好王者真好王者真好王者真好王者真好王者真好王者真好'
    # article1.categroy_id = category1.id
    #
    # db.session.add(article)
    # db.session.add(article1)
    # db.session.commit()

    # article2 = Article()
    # article2.title = '和平精英'
    # article2.desc = '和平精英真好'
    # article2.content = '和平精英真好和平精英真好和平精英真好和平精英真好和平精英真好和平精英真好'
    # article2.categroy_id = 2
    #     #
    # # db.session.add(article)
    # db.session.add(article2)
    # db.session.commit()

    # tag1 = Tag(name='游戏')
    # tag2 = Tag(name='生活')
    # tag3 = Tag(name='娱乐')
    # db.session.add(tag1)
    # db.session.add(tag2)
    # db.session.add(tag3)
    # article2 = Article()
    # article2.title = '吃鸡吃鸡'
    # article2.desc = '吃鸡吃鸡真好'
    # article2.content = '吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡吃鸡真好'
    # article2.categroy_id = 2
    # article2.tags.append(tag1)
    # article2.tags.append(tag2)
    # db.session.add(article2)
    # db.session.commit()
