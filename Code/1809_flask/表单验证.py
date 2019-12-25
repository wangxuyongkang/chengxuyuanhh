from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'python is good'


class LoginFrom(FlaskForm):
    name = StringField(label='账号',validators=[DataRequired('用户名不能为空')])
    pwd = PasswordField(label='密码',validators=[DataRequired('用户名不能为空'),EqualTo('pwd1','密码不一致')])
    pwd1 = PasswordField(label='重复密码',validators=[DataRequired('用户名不能为空')])
    submit = SubmitField(label='提交')

@app.route('/',methods=['GET','POST'])
def index ():
    form = LoginFrom()
    if form.validate_on_submit():
        name = form.name.data
        pwd = form.pwd.data
        pwd1 = form.pwd1.data
        return '登陆成功'
    return  render_template('index3.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)