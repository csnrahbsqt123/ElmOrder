from apps.models import BaseModel, db


class MenuFood(BaseModel):
    __tablename__ = "food"
    # 对外ID
    goods_id = db.Column(db.String(8), unique=True, index=True)
    # 菜品名称
    goods_name = db.Column(db.String(64))
    # 菜品评分
    rating = db.Column(db.Float, default=5.0)
    # 归属店铺
    shop_id = db.Column(db.String(16), db.ForeignKey('shop_seller.pub_id'))
    # 归属分类
    category_id = db.Column(db.String(8), db.ForeignKey('food_class.pub_id'))
    cates = db.relationship('MenuCategory', backref='foods')  # 添加一条关系
    # 菜品价格
    goods_price = db.Column(db.Float, default=0.0)
    # 菜品描述
    description = db.Column(db.String(128), default='')
    # 月销售额
    month_sales = db.Column(db.Integer, default=0)
    # 评分数量
    rating_count = db.Column(db.Integer, default=0)
    # 提示信息
    tips = db.Column(db.String(128), default='')
    # 菜品图片
    goods_img = db.Column(db.String(128), default='')

    def keys(self):
        return "goods_id", "goods_name", "rating", "goods_price", "description", "tips", "month_sales", "goods_img"


"""菜品分类"""


class MenuCategory(BaseModel):
    __tablename__ = "food_class"
    pub_id = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(128), default='')
    type_accumulation = db.Column(db.String(16))
    is_default = db.Column(db.Boolean, default=False)
    # 归属店铺
    shop_id = db.Column(db.String(16), db.ForeignKey('shop_seller.pub_id'))
    shop = db.relationship('ShopSellerModel', backref='categories')

    def keys(self):
        return "name", "description", "type_accumulation", "is_default"
