from flask import Flask
from config import configs
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
db = SQLAlchemy()
from flask_login import LoginManager

'''
http://127.0.0.1:5000/api/v1/user/login

'''
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
app = None


def create_app(type):
    global app
    app = Flask(__name__)

    babel = Babel(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
    db.init_app(app)

    adm = Admin(app,name='订餐管理后台',template_mode='bootstrap3',base_template='admin/mybase.html')

    #让登陆管理器去管理app
    login_manager.init_app(app)
    app.config.from_object(configs[type])

    return app