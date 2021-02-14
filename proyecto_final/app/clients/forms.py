from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Length, InputRequired, Email, Regexp, NumberRange


class CreateUserForm(FlaskForm):
    first_name = StringField('Nombre', render_kw={"placeholder": "test"},
                             validators=[InputRequired(message="No ingreso el nombre"),Length(max=20, message="Nombre demasiado largo")])
    last_name = StringField('Apellido', render_kw={"placeholder": "test"},
                             validators=[InputRequired(message="No ingreso el nombre"),Length(max=20, message="Nombre demasiado largo")])
    email = EmailField('Email', validators=[InputRequired(message="No ingreso un correo"),
                                            Email(message="Email invalido")])
    login_name = StringField('Nombre de Usuario', validators=[InputRequired(message="No ingreso un nombre de usuario"),
                                                              Length(max=20, message="Nombre de usuario demasiado largo")])
    password = PasswordField('Contraseña', validators=[Regexp(message="Contraseña invalida",
                                                                    regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    address = StringField('Dirección', validators=[InputRequired(message="No ingreso una dirección")])
    phone_number = IntegerField("Número Celular", validators=[NumberRange(min=10, max=10, message="Numero invalido")])