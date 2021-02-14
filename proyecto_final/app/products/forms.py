from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired

class CreateCategoryForm(FlaskForm):
    category_name = StringField('First_name', validators=[DataRequired(message="No se ingreso un nombre para la categoria"),
                                                    Length(max=20, message="Nombre demasiado largo")])


class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="No se ingreso un nombre para la categoria"),
                                           Length(max=50, message="Nombre demasiado largo")])
    image = StringField('Image URL', validators=[DataRequired(message="No se ingreso un link para la imagen")])
    price = IntegerField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(max=500)])
    refundable = SelectField('Refundable', choices=[("True", 'Yes'), ("", 'No')], coerce=bool)
    category_id = IntegerField('Category id', validators=[DataRequired()])