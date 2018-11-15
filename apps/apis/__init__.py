from flask import Blueprint

api_bp = Blueprint("api", __name__,url_prefix="/api/v1")
from apps.apis import register_login
from apps.apis import cpi_shop
from apps.apis import cpi_cart


