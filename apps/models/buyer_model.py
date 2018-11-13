from apps.models import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class BuyerModel(BaseModel):
    username = db.Column(db.String(32),unique=True)
    _password = db.Column("password", db.String(128))
    tel=db.Column(db.String(16),unique=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)
