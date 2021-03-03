from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Length, DataRequired, NumberRange, Email, InputRequired, ValidationError


class CreateUserForm(FlaskForm):
    first_name = StringField('Nombre',
                             validators=[DataRequired(), Length(max=20, message="Nombre demasiado largo")])
    last_name = StringField('Apellido',
                            validators=[DataRequired(), Length(max=20, message="Nombre demasiado largo")])
    email = EmailField('Email', validators=[DataRequired(),
                                            Length(max=20, message="Email demaasiado largo"),
                                            Email(message="Email invalido")])
    login_name = StringField('Nombre de Usuario', validators=[DataRequired(),
                                                              Length(max=20,
                                                                     message="Nombre de usuario demasiado largo")])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(max=20, min=8,
                                                                              message="La contraseña debe contener de 8 a 20 caracteres")])
    address = StringField('Dirección', validators=[DataRequired()])
    phone_number = IntegerField("Número Celular", validators=[DataRequired()])
    def validate_phone_number(form, field):
        print("len", len(str(field.data)))
        if len(str(field.data)) <10 or len(str(field.data)) >12:
            raise ValidationError('Numero invalido')


class UpdateFirstNameForm(FlaskForm):
    first_name = StringField('Nombre', validators=[InputRequired(), Length(max=20, message="Nombre demasiado largo")])


class UpdateLastNameForm(FlaskForm):
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=20, message="Nombre demasiado largo")])


class UpdateEmailForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),
                                            Length(max=20, message="Email demaasiado largo"),
                                            Email(message="Email invalido")])


class UpdateLoginNameForm(FlaskForm):
    login_name = StringField('Nombre de Usuario', validators=[DataRequired(),
                                                              Length(max=20,
                                                                     message="Nombre de usuario demasiado largo")])


class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(max=20, min=8,
                                                                              message="La contraseña debe contener de 8 a 20 caracteres")])


class UpdateAddressForm(FlaskForm):
    address = StringField('Dirección', validators=[DataRequired()])


class UpdatePhoneNumberForm(FlaskForm):
    phone_number = IntegerField("Número Celular", validators=[DataRequired()])

    def validate_phone_number(form, field):
        print("len", len(str(field.data)))
        if len(str(field.data)) <10 or len(str(field.data)) >12:
            raise ValidationError('Numero invalido')
