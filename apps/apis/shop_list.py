from flask import jsonify

from apps.apis import api_bp
from apps.models.shop_model import ShopSellerModel


@api_bp.route('/shop_list/', endpoint='shop_list', methods=['GET'])
def shop_list():
    shop=ShopSellerModel.query.all()
    data = [dict(dict(x), **{"id": x.pub_id}) for x in shop]
    return jsonify(data)




