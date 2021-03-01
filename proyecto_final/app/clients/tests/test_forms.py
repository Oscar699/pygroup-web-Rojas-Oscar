

def test_form_should_throw_error_when_not_valid_phone_number_data(app, form_phone_number):
    with app.app_context():
        form_phone_number.phone_number.data = 123
        form_phone_number.validate()
        for error in form_phone_number.phone_number.errors:
            assert error == "Numero invalido"