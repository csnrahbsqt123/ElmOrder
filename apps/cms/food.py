from flask import request, render_template, redirect, url_for
from flask_login import current_user, login_required

from apps.cms import cms_bp
from apps.forms.food_class_form import FoodClassForm
from apps.forms.food_form import FoodForm
from apps.libs.tools.tool import generate_pub_id, check_shop_pub_id, check_menu_pub_id, check_food_pub_id, \
    check_shop_cate
from apps.models import db
from apps.models.food_model import MenuCategory, MenuFood


@cms_bp.route("/add_category/<pub_id>/", endpoint="add_category", methods=['GET', 'POST'])
@login_required
def category_view(pub_id):
    """菜品分类"""
    s1 = check_shop_pub_id(pub_id)
    form = FoodClassForm(current_user, request.form)
    if request.method == "POST" and form.validate():
        fc = MenuCategory()
        fc.set_attrs(form.data)
        fc.pub_id = generate_pub_id()
        fc.shop_id = s1.pub_id
        db.session.add(fc)
        db.session.commit()
        return redirect(url_for("cms.add_category", pub_id="{}".format(s1.pub_id)))
    return render_template("foods/cate_food.html", form=form, flags="分类添加")


# @cms_bp.route("/add_category/", endpoint="add_category", methods=['GET', 'POST'])
# @login_required
# def category_view():
#     """菜品分类"""
#     form = FoodClassForm(current_user,request.form)
#     if request.method == "POST" and form.validate():
#         fc = MenuCategory()
#         fc.set_attrs(form.data)
#         fc.pub_id = generate_pub_id()
#         db.session.add(fc)
#         db.session.commit()
#         return redirect(url_for("cms.add_category"))
#     return render_template("foods/cate_food.html", form=form, flags="分类添加")


@cms_bp.route("/category_look/<pub_id>/", endpoint="category_look", methods=['GET', 'POST'])
@login_required
def food_class_view(pub_id):
    """菜品分类查看"""
    s1 = check_shop_pub_id(pub_id)
    if request.method == 'GET':
        f1 = MenuCategory.query.filter(MenuCategory.shop_id == pub_id).all()
        name = s1.shop_name
        return render_template("foods/cate_look.html", f1=f1, flags="查看", name=name)


@cms_bp.route("/update_cate/<pub_id>/<id>/", endpoint="update_cate", methods=['GET', 'POST'])
@login_required
def food_class_update_view(pub_id, id):
    """菜品分类更新"""

    m1 = check_menu_pub_id(pub_id)

    # 请求方式是post就更新数据库
    if request.method == 'POST':
        form = FoodClassForm(current_user, request.form)
        if form.validate():
            m1.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for("cms.add_category"))
    # 请求方式为get就回显内容
    else:
        form = FoodClassForm(current_user, data=dict(m1))
    return render_template("foods/cate_food.html", form=form, flags="更新")


@cms_bp.route("/add_foods/<pub_id>/", endpoint="add_foods", methods=['GET', 'POST'])
@login_required
def food_view(pub_id):
    """菜品添加"""
    s1 = check_shop_pub_id(pub_id)
    form = FoodForm(pub_id, request.form)
    if request.method == "POST" and form.validate():
        fc = MenuFood()
        fc.set_attrs(form.data)
        fc.goods_id = generate_pub_id()
        fc.shop_id = s1.pub_id
        db.session.add(fc)
        db.session.commit()
        return redirect(url_for("cms.add_foods", pub_id=s1.pub_id))
    return render_template("foods/cate_food.html", form=form, flags="菜品添加")


@cms_bp.route("/food_look/<pub_id>/", endpoint="food_look", methods=['GET', 'POST'])
@login_required
def food_look_view(pub_id):
    """菜品查看"""
    """优化后代码"""
    s1 = check_shop_pub_id(pub_id)
    items = [(x.name, x.foods) for x in s1.categories]
    # if request.method == 'GET':
    #     form = FoodForm(pub_id)
    #     classnames = form.category_id.choices
    #     f1 = MenuFood.query.filter(MenuFood.shop_id == pub_id).all()
    #     name = s1.shop_name
    return render_template("foods/food_look.html", items=items, flags="菜品查看", name=s1)


@cms_bp.route("/update_food/<goods_id>/<foods_id>/", endpoint="update_food", methods=['GET', 'POST'])
@login_required
def food_update_view(goods_id, foods_id):
    """菜品编辑"""
    f1 = check_food_pub_id(foods_id)
    s1 = check_shop_pub_id(goods_id)

    # 请求方式是post就更新数据库
    if request.method == 'POST':
        form = FoodForm(goods_id, request.form)
        if form.validate():
            f1.set_attrs(form.data)
            db.session.commit()
            return redirect(url_for("cms.food_look", pub_id=s1.pub_id))
    # 请求方式为get就回显内容
    else:
        form = FoodForm(goods_id, data=dict(f1))
        form.category_id.data = f1.category_id
    return render_template("foods/cate_food.html", form=form, flags="更新")
