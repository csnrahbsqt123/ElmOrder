from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import create_app
from apps.models import db

app = create_app("apps.settings.DevConfig")
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

@app.errorhandler(404)
def error_page(error):
    return "找不到页面"
if __name__ == '__main__':
    # print(app.config)
    manager.run()

