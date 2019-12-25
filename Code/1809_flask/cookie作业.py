from flask import Flask, render_template, request, redirect, url_for, make_response

# 创建Flask对象
app = Flask(__name__)


# 路由和视图
@app.route('/index')
# @app.route('/')
def index():
    ctx = {
        'name': 'laowang',
        'age': 12,
        'hobby': ['抽烟', '喝酒', '汤头'],
        'card': {'card': '123456', 'gender': '女'},
        'content': '<em>hello<em>',
        'password': '123456',
    }
    account = request.cookies.get('account')
    password = request.cookies.get('password')
    print(account,password)
    if account and password:
        return render_template('index.html', **ctx)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@app.route('/')
def login():

    if request.method == 'GET':
        return render_template('login.html')
    else:
        account = request.form.get('account')
        password = request.form.get('password')
        if account == '123456' and password == '123456':
            resp = make_response(render_template('login.html'))
            resp.set_cookie('account', '123456', max_age=100)

            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)