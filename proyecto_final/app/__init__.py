from flask import Flask, flash, session, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from app.db import db, ma
from flask_login import LoginManager, current_user, login_required
from flask_wtf import CSRFProtect
from conf.config import DevelopmentConfig
from app.products.views import store
from app.clients.views import userBp
from app.admins.views import adminBp
from flask_migrate import Migrate
from app.payment_methods.views import paymentMethods
from app.orders.views import order
from app.clients.models import User
from app.admins.models import AdminUser
from flask import url_for, redirect
from functools import wraps


ACTIVE_ENDPOINTS = [('/store', store), ('/user', userBp), ('/admins', adminBp), ('/payment-methods', paymentMethods), ('/order', order)]
SWAGGER_URL = '/swagger'
API_URL = '/spec'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app-name': "CompuTech Store"
    },
)


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.jinja_env.filters['zip'] = zip
    app.jinja_env.filters['len'] = len

    app.config.from_object(config)
    login_manager = LoginManager()
    csrf = CSRFProtect(app)
    migrate = Migrate(app)

    login_manager.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db=db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(swaggerui_blueprint)
    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    login_manager.login_view = "userBp.login"

    def login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash("Primero debes inicicar sesion")
                return redirect(url_for('userBp.login'))

        return wrap

    @app.route("/")
    def redirect_home():
        if current_user.is_anonymous:
            return redirect(url_for('store.home_page'))
        else:
            if str(current_user.id).isalpha():
                return redirect(url_for('adminBp.admin_panel'))
            else:
                return redirect(url_for('store.home_page'))

    @login_manager.user_loader
    def load_user(user_id):
        if user_id.isdigit():
            return User.query.get(int(user_id))
        elif user_id.isalpha():
            return AdminUser.query.filter_by(id=user_id).first()

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "CompuTech Store"
        swag['info']['Description'] = "A cool technology store"
        swag['tags'] = [{"name": "store", "description": "only the home page"},
                        {"name": "products", "description": "Everything related to the handling and presentation of the products "}]
        return jsonify(swag)

    return app


if __name__ == '__main__':
    app_flask = create_app()
    app_flask.run()
