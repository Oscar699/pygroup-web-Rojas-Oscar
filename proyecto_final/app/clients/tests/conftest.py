import pytest

from app import create_app
from app.clients.forms import UpdatePhoneNumberForm
from app.db import create_all, drop_all
from conf.config import TestConfig


@pytest.fixture
def app():
    app = create_app(config=TestConfig)
    with app.app_context():
        app.config['WTF_CSRF_ENABLED'] = False
        create_all()
        app.teardown_bkp = app.teardown_appcontext_funcs
        app.teardown_appcontext_funcs = []
        yield app  # provide the fixture value
        drop_all()

    return app


@pytest.fixture
def test_client(app):
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture
def form_phone_number(app):
    with app.app_context():
        form_phone_number = UpdatePhoneNumberForm()
        return form_phone_number

