from flask_wtf import FlaskForm
from wtforms.fields import StringField, SelectField
from wtforms.validators import DataRequired, Length


class CreatePaymentForm(FlaskForm):
    payment_code = StringField('Código', validators=[DataRequired()])
    payment_description = StringField('Descripcion', validators=[DataRequired()])


class CreateUserPayMethodForm(FlaskForm):
    payment_method_code = SelectField('Tipo de metodo de pago', choices=[('01A', 'Crédito'), ('02A', 'Débito')],
                                      validators=[DataRequired()])
    credit_card_number = StringField('Numero de tarjeta de credito', validators=[DataRequired(), Length(min=16, max=19,
                                                                                                        message="Numero de tarjeta invalido")])

