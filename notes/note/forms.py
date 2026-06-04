from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RegisterForm(FlaskForm):
    student_id = StringField(
        "学号", 
        validators=[
            DataRequired("学号不能为空"), 
            Length(4, 20, message="学号长度必须在 4 到 20 位之间"),
            Regexp(r'^[a-zA-Z0-9]+$', message="学号只能包含字母和数字")
        ]
    )
    password = PasswordField(
        "密码", 
        validators=[
            DataRequired("密码不能为空"), 
            Length(6, 40, message="密码长度必须至少为 6 位")
        ]
    )
    nickname = StringField(
        "昵称", 
        validators=[
            DataRequired("昵称不能为空"), 
            Length(2, 20, message="昵称长度必须在 2 到 20 位之间")
        ]
    )
    email = StringField(
        "邮箱", 
        validators=[
            DataRequired("邮箱不能为空"), 
            Regexp(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message="请输入有效的邮箱地址")
        ]
    )
    contact_info = StringField(
        "联系方式 (如微信/QQ/手机)", 
        validators=[
            DataRequired("联系方式不能为空"), 
            Length(2, 100, message="联系方式长度必须在 2 到 100 位之间")
        ]
    )
    verification_code = StringField(
        "验证码",
        validators=[
            DataRequired("验证码不能为空"),
            Length(6, 6, message="验证码必须为 6 位数字")
        ]
    )
    submit = SubmitField("注册")

class LoginForm(FlaskForm):
    student_id = StringField("学号", validators=[DataRequired("学号不能为空")])
    password = PasswordField("密码", validators=[DataRequired("密码不能为空")])
    submit = SubmitField("登录")

class ItemForm(FlaskForm):
    title = StringField("物品名称", validators=[DataRequired()])
    description = TextAreaField("物品描述", validators=[DataRequired()])
    story = TextAreaField("胶囊故事", validators=[DataRequired()])
    image = FileField("上传图片", validators=[FileRequired("请上传一张物品图片！"), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], "只允许上传图片！")])
    mode = SelectField("交换模式", choices=[('以物换物', '以物换物'), ('免费借用', '免费借用'), ('直接赠送', '直接赠送'), ('正常买卖', '正常买卖')], validators=[DataRequired()])
    want_item = StringField("想换物品")
    borrow_days = IntegerField("借用时长(天)")
    price = FloatField("交易金额 (元)")
    submit = SubmitField("发布")

class ExchangeForm(FlaskForm):
    message = TextAreaField("申请留言")
    submit = SubmitField("提交申请")