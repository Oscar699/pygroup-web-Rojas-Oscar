import pytest

from app.products.exceptions import ProductoNotFoundError
from app.products.models import get_product_by_id


def test_should_get_product_by_id_when_product_exists_in_db(app, product):
    with app.app_context():
        result = get_product_by_id(product.id)
        assert result["name"] == product.name


def test_should_raise_exception_when_product_does_not_exist_in_db(app):
    with pytest.raises(ProductoNotFoundError) as e:
        with app.app_context():
            get_product_by_id(22)