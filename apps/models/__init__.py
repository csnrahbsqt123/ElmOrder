from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 创建基类模型
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0)

    """自定义一个函数用来将数据写入到数据库中"""

    def set_attrs(self, a1):
        """从页面传来的数据是字典形式,需要遍历"""
        for k, v in a1.items():
            if hasattr(self, k) and k != "id":
                setattr(self, k, v)

    """将数据库数据字典化"""

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)


from apps.models import seller_model
from apps.models import shop_model
from apps.models import food_model
