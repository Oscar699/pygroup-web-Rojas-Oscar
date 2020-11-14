import sys
from http import HTTPStatus
from flask import Blueprint, Response, request, render_template

from app.products.models import (
    get_all_categories,
    create_new_category,
    get_all_products,
    get_product_by_id,
)

products = Blueprint("products", __name__, url_prefix="/products")
test = Blueprint('test', __name__, url_prefix='/Homework2flask')

EMPTY_SHELVE_TEXT = "Empty shelve!"
PRODUCTS_TITLE = "<h1> Products </h1>"
DUMMY_TEXT = "Dummy method to show how Response works"
RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}


@test.route('/<string:name>', methods=['GET'])
def resp(name):
    """Description
    Show a message on the page according to the name indicated
    in the url.

    params: name - The String name in the url.
    return: Response 200 The name is different of "pygroup"
                     400 The name is "pygroup"
    """
    if name != 'pygroup':
        return Response('Felicitaciones! Trabajo exitoso {}'.format(name), status=200)
    elif name == 'pygroup':
        return Response('ERROR! No se puede usar el nombre pygroup', status=400)

    """ 
    método render_template: La operación que convierte una plantilla en una página HTML completa se llama renderizado. 
    Para renderizar la plantilla se debe de importar una función que viene con el marco de Flask llamada 
    render_template (). Esta función toma un nombre de archivo de plantilla y una lista variable de argumentos de 
    plantilla y devuelve la misma plantilla, pero con todos los marcadores de posición en ella
    reemplazados por valores reales.

    Fuente: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
    """


@products.route("/dummy-product", methods=["GET", "POST"])
def dummy_product():
    """This method test the request types. If is GET Type it will
    render the text Products in h1 label with code 500.
    If is POST Type it will return Empty shelve! with status code 403
    """
    if request.method == "POST":
        return EMPTY_SHELVE_TEXT, HTTPStatus.FORBIDDEN

    return PRODUCTS_TITLE, HTTPStatus.INTERNAL_SERVER_ERROR


@products.route("/dummy-product-2")
def dummy_product_two():
    """This method shows how Response object could be used to make API
    methods.
    """
    return Response(DUMMY_TEXT, status=HTTPStatus.OK)


@products.route("/categories")
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


@products.route("/add-category", methods=["POST"])
def create_category():
    """

    :return:
    """
    RESPONSE_BODY["message"] = "Method not allowed"
    status_code = HTTPStatus.METHOD_NOT_ALLOWED
    if request.method == "POST":
        data = request.json
        category = create_new_category(data["name"])
        RESPONSE_BODY["message"] = "OK. Category created!"
        RESPONSE_BODY["data"] = category
        status_code = HTTPStatus.CREATED

    return RESPONSE_BODY, status_code


@products.route("/")
def get_products():
    products_obj = get_all_products()

    RESPONSE_BODY["data"] = products_obj
    RESPONSE_BODY["message"] = "Products list"

    return RESPONSE_BODY, 200


@products.route("/product/<int:id>")
def get_product(id):
    product = get_product_by_id(id)

    RESPONSE_BODY["data"] = product
    return RESPONSE_BODY, 200


@products.route("/product-stock/<int:product_id>")
def get_product_stock(product_id):
    product_stock = get_stock_by_product(product_id)
    RESPONSE_BODY["message"] = "Product stock"
    RESPONSE_BODY["data"] = product_stock

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/need-restock")
def get_products_that_need_restock():
    products_low_stock = get_products_with_low_stock()
    RESPONSE_BODY["message"] = "This products need to be re-stocked"
    RESPONSE_BODY["data"] = products_low_stock

    return RESPONSE_BODY, HTTPStatus.OK


@products.route("/register-product-stock/<int:id>", methods=["PUT", "POST"])
def register_product_refund_in_stock():

    # TODO Complete this view to update stock for product when a register for
    # this products exists. If not create the new register in DB

    status_code = HTTPStatus.CREATED
    if request.method == "PUT":
        RESPONSE_BODY["message"] = \
            "Stock for this product were updated successfully!"
        status_code = HTTPStatus.OK
    elif request.method == "POST":
        RESPONSE_BODY["message"] = \
            "Stock for this product were created successfully!"
        pass
    else:
        RESPONSE_BODY["message"] = "Method not Allowed"
        status_code = HTTPStatus.METHOD_NOT_ALLOWED
