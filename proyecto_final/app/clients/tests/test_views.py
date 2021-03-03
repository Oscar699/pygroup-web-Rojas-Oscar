from http import HTTPStatus


def test_should_return_302_when_requesting_the_root_path(app, test_client):
    with app.app_context():
        result = test_client.get('/')
        assert result.status_code == HTTPStatus.FOUND


def test_should_return_200_when_try_to_access_the_catalog_of_products(app, test_client):
    with app.app_context():
        result = test_client.get('/store/category/1/')
        assert result.status_code == HTTPStatus.OK


