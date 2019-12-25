from flask import Flask,render_template,flash,request,g

app = Flask(__name__)




@app.route('/',methods=['GET','POST'])
def index ():
    if request.method == 'GET':
        # g.uid = request.args.get('uid')
        # if g.uid == '123':
        #     return 'error'
        return  render_template('index5.html')

#只执行一次
@app.before_first_request
def before_first_request():
    print('before_first_request')

#每次都执行
@app.before_request
def before_request():
    print('before_request')

#在请求之后运行
@app.after_request
def after_request(response):
    # g.uid = '123'
    print('after_request')
    response.headers['name'] = 'haha'
    return response

#无论视图函数是否出现异常，每一次请求之后都会调用，接受一个参数，这个参数是服务器的错误信息
@app.teardown_request
def teardown_request(error):
    print('teardown_request:error {}'.format(error))

if __name__ == '__main__':
    app.run(debug=True)