from flask import Flask,session,request


app = Flask(__name__)

app.config['SECRET_KEY'] = 'shdkjashdpwohdaoifbfoial h13124lbk'


@app.route('/', methods=['GET', 'POST'])
def index():
    session['uid'] = "123456"


    return "session 案列"
@app.route('/getsession')
def getsession():
    uid = session.get('uid')
    if not uid:
        return '没有session'
    return uid


if __name__ == '__main__':
    app.run(debug=True)
