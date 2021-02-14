from http import HTTPStatus
from flask import Blueprint, Response, request, render_template
from app.products.forms import CreateCategoryForm, CreateProductForm

from app.products.models import (
    get_all_categories,
    create_new_category,
    get_all_products,
    create_new_product
)


store = Blueprint("store", __name__, url_prefix="/store")

EMPTY_SHELVE_TEXT = "Empty shelve!"
PRODUCTS_TITLE = "<h1> Products </h1>"
DUMMY_TEXT = "Dummy method to show how Response works"
RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}


# Pagina de inicio de la tienda
@store.route('/home/')
def home_page():
    """

    """
    return render_template("home.html")


# Vista para crear categorias
@store.route("/add-category", methods=["POST"])
def create_category():
    """
    :return:
    """
    form_category = CreateCategoryForm()

    if request.method == 'POST' and form_category.validate():
        message = create_new_category(name=form_category.name.data)

    return render_template('', form=form_category, message=message)


# Vista para crear productos
@store.route("/add-product", methods=["GET", "POST"])
def create_product():
    """

    """
    form_product = CreateProductForm()

    if request.method == 'POST' and form_product.validate():
        message = create_new_product(name=form_product.name.data, image=form_product.image.data, price=form_product.price.data,
                           description=form_product.description.data, refundable=form_product.refundable.data,
                           category_id=form_product.category_id.data)

    return render_template('', form=form_product, message=message)

@store.route("/")
@store.route("/categories")
def get_categories():
    """
        Verificar que si get_all_categories es [] 400, message = "No hay nada"
    :return:
    """
    categories = get_all_categories()
    status_code = HTTPStatus.OK

    if categories:
        RESPONSE_BODY["message"] = "OK. Categories List"
        RESPONSE_BODY["data"] = categories
    else:
        RESPONSE_BODY["message"] = "OK. No categories found"
        RESPONSE_BODY["data"] = categories
        status_code = HTTPStatus.NOT_FOUND

    return RESPONSE_BODY, status_code
