from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RegisterForm(FlaskForm):
    email = StringField("邮箱", validators=[DataRequired()])
    student_id = StringField("学号", validators=[DataRequired()])
    nickname = StringField("昵称", validators=[DataRequired(), Length(2,20)])
    contact_info = StringField("联系方式 (如微信/QQ)", validators=[DataRequired(), Length(2,100)])
    code = StringField("验证码", validators=[DataRequired()])
    submit = SubmitField("注册")

class LoginForm(FlaskForm):
    email = StringField("邮箱", validators=[DataRequired()])
    code = StringField("验证码", validators=[DataRequired()])
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