import pytest

from app.products.exceptions import ProductNotFoundError, StockNotFoundError
from app.products.models import get_product_by_id, get_stock_by_product_id


def test_should_get_product_by_id_when_product_exists_in_db(app, product):
    with app.app_context():
        result = get_product_by_id(product_id=product.id)
        assert result["id"] == product.id


def test_should_raise_error_when_product_does_not_exist_in_db(app):
    with pytest.raises(ProductNotFoundError) as e:
        with app.app_context():
            get_product_by_id(-1)


def test_should_get_stock_product_by_product_id_when_stock_product_exists_in_db(app, product, stock):
    with app.app_context():
        result = get_stock_by_product_id(product_id=product.id)
        assert result["product_id"] == stock.product_id


def test_should_raise_error_when_stock_product_does_not_exist_in_db(app):
    with pytest.raises(StockNotFoundError) as e:
        with app.app_context():
            get_stock_by_product_id(-1)
