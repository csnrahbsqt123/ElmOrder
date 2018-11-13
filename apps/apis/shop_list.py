import random

from flask import jsonify, request, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from apps.apis import api_bp
from apps.forms.buyer_form import BuyerRegisterForm, BuyerLoginForm
from apps.models import db
from apps.models.buyer_model import BuyerModel
from apps.models.shop_model import ShopSellerModel


@api_bp.route('/shop_list/', endpoint='shop_list', methods=['GET'])
def shop_list():
    shop = ShopSellerModel.query.all()
    data = [dict(dict(x), **{"id": x.pub_id}) for x in shop]
    return jsonify(data)


@api_bp.route("/sms/", endpoint='sms', methods=["GET"])
def get_sms_view():
    """验证码"""
    # 获取tel
    tel = request.args.get("tel")
    if tel:
        """得到电话号码,随机生成4位随机码"""
        code = [str(random.randint(0, 9)) for x in range(4)]
        code = "".join(code)
        print("验证码为:{}".format(code))
        """将电话号与随机码保存到redis中"""
        api_redis = current_app.config.get("API_REDIS")
        api_redis.setex(tel, code, current_app.config.get("SMS_LIFETIME"))
        return jsonify({"status": True, "message": "验证成功"})
    else:
        return jsonify({"status": False, "message": "不存在该号码"})


@api_bp.route("/register/", endpoint='register', methods=["POST"])
def buyer_register_view():
    """注册"""
    form = BuyerRegisterForm(request.form)
    if form.validate():
        buyer = BuyerModel()
        buyer.set_attrs(form.data)
        db.session.add(buyer)
        db.session.commit()
        return jsonify({"status": "true", "message": "注册成功"})
    else:
        return jsonify({"status": "false",
                        "message": "".join(["{}:{}".format(k, v[0]) for k, v in form.errors.items()])
                        })


@api_bp.route("/login/", endpoint='login', methods=["POST"])
def buyer_login_view():
    """登录"""
    form = BuyerLoginForm(request.form)
    if form.validate():
        """验证手机号及密码是否正确"""
        buyer = BuyerModel.query.filter_by(username=form.name.data).first()
        if buyer and buyer.check_password(form.password.data):
            s = Serializer(current_app.config.get("SECRET_KEY"), expires_in=current_app.config.get("TOKEN_EXPIRES"))
            data = s.dumps({"user_id": buyer.id})
            resp = jsonify({'status': "true", 'message': '登陆成功', 'user_id': buyer.id, 'username': buyer.username})
            resp.set_cookie('token', data.decode('ascii'))
            return resp
        else:
            return jsonify({"status": "false", "message": "手机号或密码错误"})
    else:
        return jsonify({"status": "false",
                        "message": "".join(["{}:{}".format(k, v[0]) for k, v in form.errors.items()])
                        })


