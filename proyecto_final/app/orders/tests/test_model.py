import pytest

from app.orders.exceptions import InvoiceNotFoundError
from app.orders.models import change_status_order_by_customer_id, delete_invoice_by_order_id, \
    delete_payments_by_invoice_number


def test_should_get_none_when_change_status_of_an_active_order_by_customer_id(app, order):
    with app.app_context():
        result = change_status_order_by_customer_id(customer_id=order.customer_id)
        assert result is None


def test_should_raise_error_when_invoice_does_not_exist_in_db_at_the_moment_of_try_delete_it(app):
    with pytest.raises(InvoiceNotFoundError) as e:
        with app.app_context():
            delete_invoice_by_order_id(order_id="unacosaloca")


def test_should_get_true_when_delete_a_payment_by_invoice_number(app, invoice, payment):
    with app.app_context():
        result = delete_payments_by_invoice_number(invoice_number=invoice.number)
        assert result is True
