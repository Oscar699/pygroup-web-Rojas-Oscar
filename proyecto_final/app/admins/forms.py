from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Length, DataRequired, NumberRange, Email, InputRequired, ValidationError


class CreateAdminForm(FlaskForm):
    admin_name = StringField('Nombre de admin', validators=[DataRequired(), Length(max=50, message="Nombre demasiado largo")])
    admin_password = PasswordField('Contraseña', validators=[DataRequired(), Length(max=20, min=8,
                                                                                    message="La contraseña debe contener de 8 a 20 caracteres")])
    email = EmailField('Email', validators=[DataRequired(), Length(max=20, message="Email demaasiado largo"),
                                            Email(message="Email invalido")])