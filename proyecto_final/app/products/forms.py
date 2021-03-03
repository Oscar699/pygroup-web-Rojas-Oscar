from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length


class CreateCategoryForm(FlaskForm):
    category_name = StringField('Nombre', validators=[DataRequired()])


class CreateProductForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=50, message="Nombre demasiado largo")])
    image = StringField('Imagen URL', validators=[DataRequired()])
    price = IntegerField('Precio', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired(), Length(max=500)])
    refundable = SelectField('Reembolso', choices=[("True", 'Es reembolsable'), ("", 'No reembolsable')], coerce=bool)
    category_id = IntegerField('Id de Categoria', validators=[DataRequired()])


class UpdateStockForm(FlaskForm):
    product_id = IntegerField('Id del producto', validators=[DataRequired()])
    quantity = IntegerField('Cantidad a añadir', validators=[DataRequired()])

