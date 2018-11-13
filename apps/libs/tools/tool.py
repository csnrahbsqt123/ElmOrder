import uuid
from os import abort

from apps.models.food_model import MenuCategory, MenuFood
from apps.models.shop_model import ShopSellerModel


def generate_pub_id():
    pub_id = str(uuid.uuid4())
    return "".join(pub_id.split("-")[:3])


def check_shop_pub_id(pub_id):
    s1 = ShopSellerModel.query.filter_by(pub_id=pub_id).first()
    return s1 or abort(404)


def check_menu_pub_id(pub_id):
    m1 = MenuCategory.query.filter_by(pub_id=pub_id).first()
    return m1 or abort(404)


def check_food_pub_id(pub_id):
    m1 = MenuFood.query.filter_by(goods_id=pub_id).first()
    return m1 or abort(404)


# 获得店铺对应的分类对象
def check_shop_cate(shop, cate_id):
    for cate in shop.categories:
        if cate.id == cate_id:
            return cate
    abort(404)
