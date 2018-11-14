import random

from flask import jsonify, request, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from apps.apis import api_bp
from apps.forms.buyer_form import BuyerRegisterForm, BuyerLoginForm, AddressForm

from apps.libs.tools.token_required import token_require

from apps.models.buyer_model import BuyerModel, BuyerAddress,db
from apps.models.food_model import MenuFood
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

#添加收货地址
@api_bp.route("/address/", methods=["POST"])
@token_require
def address_view():
    form = AddressForm(request.form)
    if form.validate():
        if not form.id.data:
            #说明是新添地址
            b_addr = BuyerAddress()
            b_addr.user=g.current_user
            message="添加成功"
        else:
            #说明是修改地址
            """获得该用户下所有的收货地址对象,是一个列表"""
            addresses = g.current_user.addresses
            """获得当前点击的地址对象"""
            b_addr = addresses[form.id.data - 1]
            message = "更新成功"
        b_addr.set_attrs(form.data)
        db.session.add(b_addr)
        db.session.commit()
        return jsonify({"status": "true", "message": message})
    return jsonify({"status": "false", "message": "地址添加失败"})

# 收获地址api
@api_bp.route('/address/', endpoint='address', methods=['GET'])
@token_require
def get_address_list():
    """获得该用户下所有的收货地址对象,是一个列表"""
    addresses = g.current_user.addresses
    addr_id = request.args.get('id')
    if addr_id:
        """如果获取到id,则进入更新界面"""
        return jsonify(dict(addresses[int(addr_id) - 1]))
    """如没有值,获得所有当前用户下的地址信息"""
    result = [{**dict(address), 'id': num+1} for num, address in enumerate(addresses)]
    return jsonify(result)





