from flask import Flask

from app.db import db, ma
from conf.config import DevelopmentConfig
from app.products.views import products, test
from flask_wtf import CSRFProtect

ACTIVE_ENDPOINTS = [('/products', products), ('/Homework2flask', test)]


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app


if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run(debug=True)