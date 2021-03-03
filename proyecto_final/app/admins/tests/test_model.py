from app.admins.models import create_admin_user, AdminUser, get_admin_by_email


def test_should_create_new_admin_user(app):
    with app.app_context():
        admin = create_admin_user(admin_name="RandomAdminName", admin_password="RandomAdminPasswordNotEncrypted", email="randomAdminEmail@prueba.com")
        assert isinstance(admin, AdminUser) is True


def test_should_get_admin_by_email_when_it_exist_in_data_base(app, admin):
    with app.app_context():
        email = admin.email
        result = get_admin_by_email(email=email)
        assert result["id"] == admin.id
