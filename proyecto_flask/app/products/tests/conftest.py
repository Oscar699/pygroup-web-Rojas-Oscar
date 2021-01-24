import pytest
import sqlalchemy

from app import create_app
from app.db import create_all, db, drop_all
from app.products.models import Product, Category
from conf.config import TestingConfig
from app.products.forms import CreateCategoryForm

@pytest.fixture
def app():
    app = create_app(config=TestingConfig)
    with app.app_context():
        create_all()
        app.teardown_bkp = app.teardown_appcontext_funcs
        app.teardown_appcontext_funcs = []
        yield app
        drop_all()

    return app

@pytest.fixture
def product(app):
    with app.app_context():
        product = Product(name="fake-product", price=1, description="this",
                          refundable=True)
        db.session.add(product)
        db.session.commit()
        return product

@pytest.fixture
def category(app):
    with app.app_context():
        category = Categoty(name="fake_category")
        db.session.add(category)
        db.session.commit()
        return category


@pytest.fixture
def test_client(app):
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture
def form_category(app):
    with app.app_context():
        form_category = CreateCategoryForm()
        if request.method == 'POST' and form_product.validate():
            create_new_product(name=form_product.name.data, image=form_product.image.data,
                               price=form_product.price.data, weight=form_product.weight.data,
                               description=form_product.description.data, refundable=form_product.refundable.data,
                               category_id=form_product.category_id.data)
            return ""
