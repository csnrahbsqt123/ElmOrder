import json

from flask import request, current_app, g, jsonify

from apps.apis import api_bp
from apps.libs.tools.token_required import token_require
from apps.models.food_model import MenuFood


@api_bp.route("/cart/", methods=["GET"])
@token_require
def cart_show_view():
    """获取购物车数据"""
    user = g.current_user
    api_redis = current_app.config.get('API_REDIS')
    cart_key = 'cart_{}'.format(user.id)
    goods = api_redis.hgetall(cart_key)
    total = 0
    result = []
    for gid, info in goods.items():
        good_info = json.loads(info)
        good_info['goods_id'] = gid.decode('ascii')
        total += (good_info['goods_price'] * int(good_info['amount']))
        result.append(good_info)
    return jsonify({'goods_list': result, 'totalCost': total})


@api_bp.route("/cart/", methods=["POST"])
@token_require
def cart_add_view():
    """添加购物车数据"""
    goods_ids = request.form.getlist("goodsList[]")
    goods_num = request.form.getlist("goodsCount[]")
    api_redis = current_app.config.get("API_REDIS")
    if len(goods_num) and len(goods_ids):
        user = g.current_user
        cart_key = "cart_{}".format(user.id)
        for gid, num in zip(goods_ids, goods_num):
            food = MenuFood.query.filter_by(id=gid).first()
            food_info = {
                'amount': num,
                'goods_name': food.goods_name,
                'goods_price': food.goods_price,
                'goods_img': food.goods_img,
            }
            api_redis.hset(cart_key, gid, json.dumps(food_info))
            api_redis.expire(cart_key, current_app.config.get('CART_LIFETIME', 3600))
        return jsonify({'status': 'true', 'message': '添加成功'})
    else:
        return jsonify({'status': 'false', 'message': '无食品数据'})
