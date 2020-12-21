
from flask import Flask
from flask_wtf import CSRFProtect

from app.auth.models import User
from app.auth.views import auth
from app.db import db, ma
from conf.config import DevelopmentConfig
from app.products.views import products, homework
from flask_migrate import Migrate
from flask_login import LoginManager

ACTIVE_ENDPOINTS = [('/products', products), ('/Homework2flask', homework), ('', auth)]


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    migrate = Migrate()
    csrf = CSRFProtect(app)
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"

    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db=db)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(user_id)

    csrf.exempt(products)
    csrf.exempt(auth)
    return app


if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run(debug=True)