from flask import Blueprint

api_bp = Blueprint("api", __name__,url_prefix="/api/v1")
from apps.apis import shop_list


