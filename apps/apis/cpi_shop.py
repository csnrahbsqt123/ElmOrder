from flask import jsonify, request

from apps.apis import api_bp
from apps.models.food_model import MenuFood
from apps.models.shop_model import ShopSellerModel


@api_bp.route("/shop/", endpoint="shop", methods=["GET"])
def shop_view():
    shop_id = request.args.get("id")
    shop = ShopSellerModel.query.filter_by(pub_id=shop_id).first()
    if not shop:
        return jsonify({"error": "No Shop"})
    cates = shop.categories
    a = [{**dict(cate),
        "goods_list": [{
            **dict(i),
            "goods_id": i.id
        } for i in cate.foods]
    } for cate in cates]
    data = {**dict(shop), 'id': shop.pub_id, 'commodity': a, 'evaluate': []}
    return jsonify(data)
