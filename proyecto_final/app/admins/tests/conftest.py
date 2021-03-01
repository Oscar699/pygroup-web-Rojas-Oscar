import pytest

from app import create_app, AdminUser
from app.admins.forms import CreateAdminForm
from app.db import db, create_all, drop_all
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
def admin(app):
    with app.app_context():
        admin = AdminUser(id="randomAdminId", admin_name="RandomAdminName", admin_password="RandomAdminPasswordNotEncrypted", email="randomAdminEmail@prueba.com")
        db.session.add(admin)
        db.session.commit()
        return admin

@pytest.fixture
def form_admin(app):
    with app.app_context():
        form_admin = CreateAdminForm()
        return form_admin
