from flask import Flask

from app.db import db, ma
from flask_login import LoginManager
from conf.config import DevelopmentConfig
from app.products.views import store
from app.clients.views import userBp
from app.clients.models import User
from flask_migrate import Migrate


ACTIVE_ENDPOINTS = [('/store', store), ('/user', userBp)]


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config)
    migrate = Migrate()
    login_manager = LoginManager()

    login_manager.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db=db)

    with app.app_context():
        db.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    login_manager.login_view = "userBp.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


if __name__ == '__main__':
    app_flask = create_app()
    app_flask.run()
