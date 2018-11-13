from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, login_required, current_user
from qiniu import Auth
from apps.cms import cms_bp
from apps.forms.seller_form import ClientUserForm, ClientLoginForm
from apps.models import db
from apps.models.seller_model import ClientUserModel
from apps.models.shop_model import ShopSellerModel



@cms_bp.route("/", endpoint="index")
def index_view():
    return render_template("user/index.html")


# 保护视图函数
@cms_bp.route("/vip/", endpoint="vip")
@login_required
def vip_view():
    s = request.cookies.get("session")
    print(s)
    return "vip"


# 注册
@cms_bp.route("/register/", endpoint="register", methods=["GET", "POST"])
def register_view():
    form = ClientUserForm(request.form)
    # 验证是否是post请求和数据是否合法
    if request.method == "POST" and form.validate():
        # 合法,将数据加入到数据库中
        user = ClientUserModel()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        # 跳转到登录界面
        return redirect(url_for("cms.login"))
    return render_template("user/reg_login.html", form=form, flags="注册")


@cms_bp.route("/login/", endpoint="login", methods=["GET", "POST"])
def login_view():
    form = ClientLoginForm(request.form)
    if request.method == "POST" and form.validate():
        u1 = ClientUserModel.query.filter_by(username=form.username.data).first()
        if u1 and u1.check_password(form.password.data):
            # 添加session
            login_user(u1)
            # 跳转到首页
            return redirect(url_for("cms.index"))
        else:
            form.password.errors = ["用户名或密码错误", ]
    return render_template("user/reg_login.html", form=form, flags="登录")


@cms_bp.route("/center/", endpoint="center", methods=["GET", "POST"])
@login_required
def center_view():
    id = current_user.id
    sellers = ShopSellerModel.query.filter(ShopSellerModel.seller_id == id).all()
    return render_template("user/person_center.html", sellers=sellers)


@cms_bp.route('/uptoken/', endpoint='uptoken')
def get_token():
    access_key = 'j1deCRtoWH3iLEcIAdPPY3PkgLHEUc4vrT6hO9CU'
    secret_key = 'ItMAnK-rMf4K2yBl10217AbtumXx_ecd7y82xwtV'

    q = Auth(access_key=access_key, secret_key=secret_key)
    token = q.upload_token('elmorder')
    return jsonify({"uptoken": token})