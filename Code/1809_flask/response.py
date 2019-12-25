from flask import Flask, render_template, request, send_from_directory, make_response, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    resp = make_response(render_template('cookie.html'))
    resp.set_cookie('name', 'laowang', max_age=10)
    resp.set_cookie('gender', 'woman', expires=datetime(2019, 6, 1))
    resp.delete_cookie('name')
    resp.headers['age'] = 12
    return resp


@app.route('/getcookie', methods=['GET', 'POST'])
@app.route('/')
def getcookie():
    data = request.cookies
    print(data)

    return '获取cookie' + str(data)


@app.route('/json')
def json():
    resp = {"code": 1, "msg": "成功", "data": {
        'infos': [
            {'name': 'laowang',
             "age": 12,
             "gender": "女",
             },
            {'name': 'laowang',
             "age": 12,
             "gender": "女",
             },
            {'name': 'laowang',
             "age": 12,
             "gender": "女",
             },
        ]
    }}
    return jsonify(resp)  # 把json序列化
    # 序列化 把对象变成可传输或可储存的过程叫序列化
    # 反序列化 把可传输可储存的数据转换为对象叫反序列化


if __name__ == '__main__':
    app.run(debug=True)
