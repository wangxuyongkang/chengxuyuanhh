from flask import Flask,render_template,request,send_from_directory
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif','cfg'])
app.config.from_pyfile('config.cfg')

def isallow(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS


#路由和视图
@app.route('/register',methods=['GET','POST'])
@app.route('/')
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        account =  request.form.get('account')
        password = request.form.get('password')
        hobby = request.form.getlist('hobby')#一键多值
        return account+password+str(hobby)

#重定向
from flask import redirect,url_for
@app.route('/login',methods=['GET','POST'])
def login ():
    print(request.url)
    print(request.path)
    print(request.headers)
    print(request.cookies)
    print("values:",request.values)
    print(request.full_path)
    if request.method == 'GET':
        account = request.args.get('account')
        password = request.args.get('password')
        if not account and not password:
            return render_template('login.html')
        elif account=='123456' and password == '123456':
            return redirect(url_for('article'))
        else:
            return account+password

from datetime import datetime
@app.route('/article')
def article():

    ext = {
        'title':'我的爸爸',
        'times': datetime.now(),
        'center':'那天我回到家，咦? 爸爸呢',
    }
    return render_template('article.html',**ext)



def handletime(time,mode):
    return time.strftime(mode)


app.jinja_env.filters['handletime'] = handletime  # 注册过滤器
#当前是时间获取函数


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        file = request.files.get('file')
        if not file:
            return redirect(request.url)
        if isallow(file.filename):
            filename = secure_filename(file.filename)#文件名做校验
            file.save(os.path.join(app.config.get('UPLOAD_FOLDER'),file.filename))
            return redirect(url_for('show',filename=file.filename))
    #1.jpg
    #1.1.jpg
    #1.1.1.jpg
@app.route('/show/<filename>')
def show(filename):
    return send_from_directory(app.config.get('UPLOAD_FOLDER'),filename)




if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000',debug=True)