from flask import Blueprint
app_home = Blueprint('bp_home',__name__,template_folder='templates')

from .home import home