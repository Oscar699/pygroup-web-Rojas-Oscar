from app.payment_methods.models import get_customer_payment_method_by_id, delete_customer_payment_method_by_id, \
    get_customer_payment_methods_by_customer_id


def test_should_get_customer_payment_method_by_id_when_it_exists_in_db(app, customer_payment_method):
    with app.app_context():
        result = get_customer_payment_method_by_id(id=customer_payment_method.id)
        assert result["id"] == customer_payment_method.id


def test_should_get_true_when_customer_payment_method_is_deleted(app, customer_payment_method):
    with app.app_context():
        id = customer_payment_method.id
        result = delete_customer_payment_method_by_id(id=id)
        assert result is True


def test_should_get_none_when_customer_does_not_exist_in_bd(app):
    with app.app_context():
        result = get_customer_payment_methods_by_customer_id(customer_id=1)
        assert result is None
