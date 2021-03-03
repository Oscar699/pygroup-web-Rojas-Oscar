import pytest

from app import create_app
from app.db import db, create_all, drop_all
from app.orders.models import Order, OrderItem, Invoice, Payment
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
def order(app):
    with app.app_context():
        order = Order(id="OI0", customer_id=1, order_status_code="OS1", order_details="En proceso")
        db.session.add(order)
        db.session.commit()
        return order

@pytest.fixture
def order_item(app):
    with app.app_context():
        order_item = OrderItem(product_id=1, order_id=1, order_item_status_code="OSI2",
                               order_item_quantity=1, order_item_price=100000, other_order_item_details="Valido")
        db.session.add(order_item)
        db.session.commit()
        return order_item


@pytest.fixture
def invoice(app):
    with app.app_context():
        invoice = Invoice(number=0, order_id=1, invoice_status_code="IS2", invoice_details="Factura pagada por Crédito")
        db.session.add(invoice)
        db.session.commit()
        return invoice

@pytest.fixture
def payment(app):
    with app.app_context():
        payment = Payment(id=0, invoice_number=0, payment_amount=119000)
        db.session.add(payment)
        db.session.commit()
        return payment
