from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    student_id = StringField("学号", validators=[DataRequired()])
    nickname = StringField("昵称", validators=[DataRequired(), Length(2,20)])
    password = PasswordField("密码", validators=[DataRequired(), Length(6,20)])
    submit = SubmitField("注册")

class LoginForm(FlaskForm):
    student_id = StringField("学号", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    submit = SubmitField("登录")

class ItemForm(FlaskForm):
    title = StringField("物品名称", validators=[DataRequired()])
    description = TextAreaField("物品描述", validators=[DataRequired()])
    story = TextAreaField("胶囊故事", validators=[DataRequired()])
    image_url = StringField("图片链接", validators=[DataRequired()])
    mode = StringField("交换模式", validators=[DataRequired()])
    want_item = StringField("想换物品")
    borrow_days = IntegerField("借用时长(天)")
    submit = SubmitField("发布")

class ExchangeForm(FlaskForm):
    message = TextAreaField("申请留言")
    submit = SubmitField("提交申请")