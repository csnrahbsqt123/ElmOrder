from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix='/api/v1',static_folder='../web_client', static_url_path='')
from apps.apis import shop_list


