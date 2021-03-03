import pytest

from app import create_app
from app.db import db, create_all, drop_all
from app.products.models import Product, Stock
from conf.config import TestConfig


@pytest.fixture
def app():
    app = create_app(config=TestConfig)
    with app.app_context():
        create_all()
        app.teardown_bkp = app.teardown_appcontext_funcs
        app.teardown_appcontext_funcs = []
        yield app  # provide the fixture value
        drop_all()

    return app


@pytest.fixture
def product(app):
    with app.app_context():
        product = Product(name="fake-product", price=1, description="desc",
                          refundable=True, category_id=1)
        db.session.add(product)
        db.session.commit()
        return product

@pytest.fixture
def stock(app):
    with app.app_context():
        stock = Stock(product_id=1, quantity=1)
        db.session.add(stock)
        db.session.commit()
        return stock
