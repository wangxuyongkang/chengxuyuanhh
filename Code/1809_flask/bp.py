from flask import Flask
from home.home import  app_home
app = Flask(__name__)

app.register_blueprint(app_home,url_prefix='/user')

@app.route('/',methods=['GET','POST'])
def index ():
    return  'index'

if __name__ == '__main__':
    app.run(debug=True)