from wtforms import Form, StringField, validators, PasswordField
from wtforms.validators import Regexp

from apps.models.seller_model import ClientUserModel


# 登录模型
class ClientLoginForm(Form):
    username = StringField(label="用户名", validators=[
        validators.DataRequired(message="用户名必填")],
                           render_kw={'class': 'form-control', 'placeholder': '请输入用户名或手机号'}
                           )
    password = PasswordField(label="登录密码", validators=[
        validators.DataRequired(message="密码必填")],
                             render_kw={'class': 'form-control', 'placeholder': '请输入密码'}
                             )


# 注册模型
class ClientUserForm(Form):
    username = StringField(label="用户名", validators=[
        validators.DataRequired(message="用户名必填"),
        validators.Length(6, 16, message="密码长度为6-16位"),
        Regexp('^([A-Za-z][A-Za-z0-9_.]*$)|(^1[3578]\d{9}$)', 0, '格式必须是字母开头,字母和数字_.组合,或者是电话号码'), ],
                           render_kw={'class': 'form-control', 'placeholder': '请输入用户名或手机号'}
                           )
    password = PasswordField(label="登录密码", validators=[
        validators.DataRequired(message="密码必填"),
        validators.Length(6, 16, message="密码长度为6-16位"),
    ],
                             render_kw={'class': 'form-control', 'placeholder': '请输入密码'}
                             )
    pwd = PasswordField(label="确认密码", validators=[
        validators.EqualTo('password', '两次密码不一致'),
        validators.DataRequired("确认密码必填"),
    ],
                        render_kw={'class': 'form-control', 'placeholder': '请输入确认密码'}
                        )

    # 检测用户名是否被注册
    def validate_username(self, obj):
        username = obj.data
        res = ClientUserModel.query.filter(ClientUserModel.username == username).first()
        if res:
            raise validators.ValidationError("该用户已被注册")
