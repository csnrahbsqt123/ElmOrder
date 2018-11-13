from flask import current_app
from wtforms import Form, StringField, validators, PasswordField

from apps.models.buyer_model import BuyerModel


class BuyerLoginForm(Form):
    """买家登录"""
    name = StringField(validators=[
        validators.DataRequired(message="用户名未填写"),
        validators.Length(3, 32, message="用户名长度为3-32位")
    ])
    password = PasswordField(validators=[
        validators.DataRequired(message="密码未填写"),
        validators.Length(6, 32, message="密码长度为6-32位")
    ])


class BuyerRegisterForm(Form):
    """买家注册"""
    username = StringField(validators=[
        validators.DataRequired(message="用户名未填写"),
        validators.Length(3, 32, message="用户名长度为3-32位")
    ])
    password = PasswordField(validators=[
        validators.DataRequired(message="密码未填写"),
        validators.Length(6, 32, message="密码长度为6-32位")
    ])
    tel = StringField(validators=[
        validators.DataRequired(message="电话号未填写"),
        validators.Regexp(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18['
                          r'0-9])|166|198|199)\d{8}$', message="请输入正确的电话号码")
    ])
    sms = StringField(validators=[validators.DataRequired(message="请输入验证码")])

    # 自定义验证用户名是否已经注册
    def validate_username(self, obj):
        name = obj.data
        b1 = BuyerModel.query.filter_by(username=name).first()
        if b1:
            raise validators.ValidationError("该用户名已经存在")

    # 自定义验证电话号码是否已经注册
    def validate_tel(self, obj):
        tel = obj.data
        b1 = BuyerModel.query.filter_by(tel=tel).first()
        if b1:
            raise validators.ValidationError("该电话号码已被注册")

    # 自定义验证验证码是否正确
    def validate_sms(self, obj):
        api_redis = current_app.config.get("API_REDIS")
        # 获取redis中的验证码
        code = api_redis.get(self.tel.data).decode("ascii")
        if not code:
            raise validators.ValidationError("没有验证码，请点击发送验证码")
        elif obj.data != code:
            raise validators.ValidationError("验证码不正确")


class AddressForm(Form):
    name = StringField(validators=[
        validators.DataRequired(message="收货人姓名未填写"),
        validators.Length(2, 16, message="用户名长度为2-16位")
    ])
    tel = StringField(validators=[
        validators.DataRequired(message="收货人电话号码未填写"),
        validators.Regexp(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18['
                          r'0-9])|166|198|199)\d{8}$', message="请输入正确的电话号码")
    ])
    detail_address= StringField(validators=[
        validators.DataRequired(message="详细收货地址未填写"),
        validators.Length(max=16, message="详细地址最多16个字符")
    ])
    provence=StringField(validators=[
        validators.DataRequired(message="省份未填写"),
        validators.Length(max=4, message="省份最多4个字符")
    ])
    city = StringField(validators=[
        validators.DataRequired(message="市级未填写"),
        validators.Length(max=8, message="市级最多8个字符")
    ])
    area = StringField(validators=[
        validators.DataRequired(message="县区未填写"),
        validators.Length(max=8, message="县区最多8个字符")
    ])
