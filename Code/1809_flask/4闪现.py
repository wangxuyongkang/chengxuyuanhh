from flask import Flask,render_template,flash,request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'python is good'



@app.route('/',methods=['GET','POST'])
def index ():
    if request.method == 'GET':
        return  render_template('index4.html')
    name = request.form.get('name')
    flash('参数错误',category='fail')
    flash('参数成功',category='success')
    return render_template('index4.html')
if __name__ == '__main__':
    app.run(debug=True)