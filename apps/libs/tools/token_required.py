# 登录验证
from functools import wraps

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from flask import request, jsonify, current_app, g

from apps.models.buyer_model import BuyerModel


def token_require(fn):
    @wraps(fn)
    def verify_login(*args, **kwargs):
        """先获取token,看是否存在"""
        token = request.cookies.get("token")
        if not token:
            """token不存在"""
            return jsonify({"status": "false", "message": "token不存在"})
        s = Serializer(current_app.config.get("SECRET_KEY"))
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return jsonify({'status': "false", 'message': '无效的token'})
        # 获取user
        user_id = data.get("user_id")
        user = BuyerModel.query.get(user_id)
        if not user:
            return jsonify({'status': "false", 'message': '非法用户'})
        g.current_user = user
        return fn(*args, **kwargs)
    return verify_login
