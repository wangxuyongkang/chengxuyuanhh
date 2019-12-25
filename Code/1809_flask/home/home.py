from . import app_home
from flask import render_template
@app_home.route('/home')
def home():
    return render_template('index1.html')