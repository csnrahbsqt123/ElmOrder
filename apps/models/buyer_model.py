from apps.models import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class BuyerModel(BaseModel):
    username = db.Column(db.String(32), unique=True)
    _password = db.Column("password", db.String(128))
    tel = db.Column(db.String(16), unique=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)


class BuyerAddress(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('buyer_model.id'))
    user = db.relationship("BuyerModel", backref="addresses")
    # 省
    provence = db.Column(db.String(8))
    # 市
    city = db.Column(db.String(16))
    # 县
    area = db.Column(db.String(16))
    # 详细地址
    detail_address = db.Column(db.String(64))
    # 收货人姓名
    name = db.Column(db.String(32))
    # 收货人电话
    tel = db.Column(db.String(16))

    def keys(self):
        return "provence", "city", "area", "detail_address", "name", "tel"
