from app.interceptor import *
from app import app
from app.admin import admin_page

from app.api.v1 import create_blueprint_v1
app.register_blueprint(admin_page, url_prefix='/admin')
app.register_blueprint(create_blueprint_v1(),url_prefix='/api/v1')
