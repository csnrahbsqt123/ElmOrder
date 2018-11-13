from flask import request, redirect, url_for, render_template
from flask_login import current_user, login_required

from apps.cms import cms_bp
from apps.forms.shop_form import ShopForm
from apps.libs.tools.tool import generate_pub_id, check_shop_pub_id
from apps.models import db
from apps.models.shop_model import ShopSellerModel


@cms_bp.route("/seller_shop/", endpoint="seller_shop", methods=['GET', 'POST'])
@login_required
def shop_view():
    form = ShopForm(request.form)
    if request.method == 'POST' and form.validate():
        s1 = ShopSellerModel.query.filter_by(shop_name=form.shop_name.data).first()
        if s1:
            form.shop_name.errors=["店铺名已存在,若是相同店名,请添加(***店)"]
        else:
            s1=ShopSellerModel()
            s1.set_attrs(form.data)
            s1.pub_id = generate_pub_id()
            s1.seller = current_user
            db.session.add(s1)
            db.session.commit()
            return redirect(url_for("cms.index"))
    return render_template("user/add_cls.html", form=form, flags="添加店铺")


@cms_bp.route("/update_shop/<pu_id>/", endpoint="update_shop", methods=['GET', 'POST'])
@login_required
def update_shop_view(pu_id):
    s1 = check_shop_pub_id(pu_id)
    # 请求方式是post就更新数据库
    if request.method == 'POST':
        form = ShopForm(request.form)
        if form.validate():
            s1.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for("cms.index"))
    # 请求方式为get就回显内容
    else:
        form=ShopForm(data=dict(s1))
    return render_template("user/add_cls.html", form=form, flags="店铺编辑")
