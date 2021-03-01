import pytest

from app import create_app
from app.db import db, create_all, drop_all
from app.payment_methods.models import CustomerPaymentMethod
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


@pytest.fixture()
def customer_payment_method(app):
    with app.app_context():
        customer_payment_method = CustomerPaymentMethod(customer_id=1, payment_method_code="01A",
                                                        credit_card_number="12345678910111",
                                                        payment_method_details="Crédito")
        db.session.add(customer_payment_method)
        db.session.commit()
        return customer_payment_method
