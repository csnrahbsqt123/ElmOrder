from flask import Flask
from flask_login import LoginManager
from flask_session import Session

login_manager = LoginManager()


def register_db(app):
    from apps.models import db
    db.init_app(app)


def register_bp(app):
    """接收蓝图"""
    from apps.cms import cms_bp
    app.register_blueprint(cms_bp)


def register_api_bp(app):
    from apps.apis import api_bp
    app.register_blueprint(api_bp)

def create_app(dev_config):
    app = Flask(__name__, static_url_path="/static", static_folder="./cms_static")
    app.config.from_object(dev_config)
    Session(app=app)
    login_manager.init_app(app)
    login_manager.login_view = "cms.login"
    register_db(app)
    register_bp(app)
    return app

def create_api_app(dev_config):
    app = Flask(__name__, static_folder='./web_client', static_url_path='')
    app.config.from_object(dev_config)
    register_db(app)
    register_api_bp(app)
    return app
