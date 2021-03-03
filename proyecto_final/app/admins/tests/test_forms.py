

def test_form_should_throw_error_when_not_valid_admin_email_data(app, form_admin):
    with app.app_context():
        form_admin.email.data = "emailInvalido"
        form_admin.validate()
        for error in form_admin.email.errors:
            assert error == "Email invalido"
