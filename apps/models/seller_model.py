from apps import login_manager
from apps.models import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 用户模型
class ClientUserModel(BaseModel,UserMixin):
    __tablename__ = "client"
    username = db.Column(db.String(32))
    _password = db.Column("password", db.String(128))

    """自定义密码加盐函数"""

    # 先定义一个函数来读取属性
    @property
    def password(self):
        return self._password

    # 在定义一个相同名的函数来写入数据
    @password.setter
    def password(self, v1):
        self._password = generate_password_hash(v1)

    # 定义函数来检测密码是否正确
    def check_password(self, data):
        return check_password_hash(self.password, data)
@login_manager.user_loader
def load_user(userid):
    return ClientUserModel.query.get(int(userid))
