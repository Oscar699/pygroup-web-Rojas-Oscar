from http import HTTPStatus
from flask import Blueprint, Response, request, render_template, flash
from flask_login import login_required

from app.products.forms import CreateCategoryForm, CreateProductForm, UpdateStockForm

from app.products.models import (
    create_stock_by_product,
    update_product_stock,
    get_product_by_id,
    get_all_categories,
    create_new_category,
    get_all_products,
    create_new_product,
    get_products_by_category,
    get_category_by_id
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
    Redirect home page
    ---
    tags:
        - store
    description: Redirects the user from the root path to the homepage
    responses:
        302:
          description: The URL has been changed
    """
    return render_template("home.html")


# Vista para crear categorias
@store.route("/add-category/", methods=["GET", "POST"])
def create_category():
    """
    :return:
    """
    form_category = CreateCategoryForm()
    message = ""

    if request.method == 'POST' and form_category.validate():
        message = create_new_category(category_name=form_category.category_name.data)

    return render_template('add-category-form.html', form=form_category, message=message)


# Vista para crear productos
@store.route("/add-product/", methods=["GET", "POST"])
@login_required
def create_product():

    form_product = CreateProductForm()
    categories = get_all_categories()
    message = ""
    if request.method == 'POST' and form_product.validate():
        message = create_new_product(name=form_product.name.data, image=form_product.image.data, price=form_product.price.data,
                                     description=form_product.description.data, refundable=form_product.refundable.data,
                                     category_id=form_product.category_id.data)

    flash(form_product.errors)

    return render_template('add-product-form.html', form=form_product, message=message, categories=categories)


@store.route("/update-stock", methods=['GET', 'POST'])
@login_required
def update_stock():
    """
        Render stock form and update stock data in db
        ---
        tags:
            - products
        get:
            summary: Render the stock form
            description: Render the form to update or add the stock of a product
            responses:
                200:
                  description: Successful rendering
    """
    form_stock = UpdateStockForm()
    message = ""
    if request.method == "POST" and form_stock.validate():
        product_id = form_stock.product_id.data
        quantity = form_stock.quantity.data
        product = get_product_by_id(product_id=product_id)
        if product:
            stock_result = update_product_stock(product_id=product_id, new_quantity=quantity)
            if stock_result:
                message = stock_result
            else:
                message = create_stock_by_product(product_id=form_stock.product_id.data, quantity=form_stock.quantity.data)
        else:
            message = "El producto referido no existe"
            response = HTTPStatus.NOT_FOUND

    print(message)
    return render_template('update-stock.html', message=message, form=form_stock), response


# Vista para un catalogo de productos segun su categoria
@store.route("/category/<category_id>/", methods=['GET'])
def show_products_by_category(category_id):
    """
    Displays a catalog of products
    ---
    tags:
        - products
    description: Displays a catalog of products according to the indicated category
    parameters:
        - in: path
          name: category_id
          description: The id of the category corresponding to the product group
          type: integer
    responses:
        200:
          description: Render the template with the products of the category
        404:
          description: There is no products to show
    """
    products = get_products_by_category(category_id=category_id)
    category = get_category_by_id(category_id=category_id)
    if products:
        response = HTTPStatus.NOT_FOUND
    else:
        response = HTTPStatus.OK
    return render_template("products_catalog.html", products=products, category=category), response


@store.route("/product/view/<product_id>/<string:cart_response>/")
def show_product_view(product_id, cart_response):
    """
        Displays product full view
        ---
        tags:
            - products
        description: Shows a more detailed view of the product, with its characteristics.
        parameters:
            - in: path
              name: product_id
              description: The id of the product
              type: integer
            - in: path
              name: cart_response
              description: The identifier of the response to "buy"
              type: string
        responses:
            200:
              description: Render the template with the full view product.
    """
    if cart_response == "Added":
        message = "Añadido al carrito satisfactoriamente"
    elif cart_response == "Exist":
        message = "Ya has añadido este producto, si quieres añadir mas ve al carrito"
    elif cart_response == "Error":
        message = "Fatal_Error"
    else:
        message = ""
    product = get_product_by_id(product_id)
    return render_template("product-view.html", product=product, message=message)
