from flask import Flask,abort


app = Flask(__name__)


@app.route('/<uid>',methods=['GET','POST'])
def index(uid):
    if uid == "123456":
        abort(404)
    return 'index'

@app.errorhandler(404)
def error_404(error):
    return '服务器迷路了'



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)