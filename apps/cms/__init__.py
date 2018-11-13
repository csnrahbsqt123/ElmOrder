from flask import Blueprint
cms_bp=Blueprint("cms",__name__)

from apps.cms import user
from apps.cms import shop
from apps.cms import food