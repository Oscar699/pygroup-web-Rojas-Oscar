from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired


class CreateCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Invalid data"), Length(max=20, message="Invalid data")])


class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50, message="Invalid data")])
    image = StringField('Image URL', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired(), Length(max=500, message="Invalid data")])
    refundable = SelectField('Refundable', choices=[("True", 'Yes'), ("", 'No')], coerce=bool)
    category_id = IntegerField('Category id', validators=[DataRequired()])
