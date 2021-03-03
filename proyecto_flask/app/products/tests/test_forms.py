import pytest

# TODO Complete test to validate form data


def test_form_should_throw_error_when_not_valid_data(app, form_category):
    with app.app_context():
        form_category.validate()
        for error in form_category.name.errors:
            assert error == "Invalid data"

