from wtforms import Form, StringField, validators, PasswordField

from apps.models.buyer_model import BuyerModel


class BuyerLoginForm(Form):
    name = StringField(validators=[
        validators.DataRequired(message="用户名未填写"),
        validators.Length(3, 32, message="用户名长度为3-32位")
    ])
    password = PasswordField(validators=[
        validators.DataRequired(message="密码未填写"),
        validators.Length(6, 32, message="密码长度为6-32位")
    ])


class BuyerRegisterForm(Form):
    username = StringField(validators=[
        validators.DataRequired(message="用户名未填写"),
        validators.Length(3, 32, message="用户名长度为3-32位")
    ])
    password = PasswordField(validators=[
        validators.DataRequired(message="密码未填写"),
        validators.Length(6, 32, message="密码长度为6-32位")
    ])
    tel = StringField(validators=[
        validators.DataRequired(message="电话号为填写"),
        validators.Regexp(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18['
                          r'0-9])|166|198|199)\d{8}$', message="请输入正确的电话号码")
    ])
    sms = StringField(validators=[validators.DataRequired(message="请输入验证码")])

    # 自定义验证用户名是否已经注册
    def validate_username(self, obj):
        name = obj.data
        b1=BuyerModel.query.filter_by(username=name).first()
        if b1:
            raise validators.ValidationError("该用户名已经存在")

    # 自定义验证电话号码是否已经注册
    def validate_tel(self, obj):
        tel = obj.data
        b1 = BuyerModel.query.filter_by(username=tel).first()
        if b1:
            raise validators.ValidationError("该电话号码已被注册")


