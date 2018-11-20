from apps import create_app

cms_app = create_app("apps.settings.DevConfig")

if __name__ == '__main__':
    from apps.models import db

    with cms_app.app_context():
        db.create_all()
    cms_app.run(host='0.0.0.0', port=9800)
