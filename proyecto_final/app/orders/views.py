from http import HTTPStatus

from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required

from app.products.models import get_product_by_id
from app.payment_methods.models import get_customer_payment_methods_by_customer_id, get_ref_payment_methods, get_customer_payment_method_by_id
from app.orders.models import (
    get_order_in_process_by_customer_id,
    create_order_item,
    get_order_item_by_product_id,
    get_order_items_by_order_id,
    delete_order_item_by_id,
    create_invoice,
    create_payment,
    change_status_order_by_customer_id
)

from app.orders.models import create_order

order = Blueprint("order", __name__, url_prefix="/order")


@order.route("/add-order-item", methods=['POST'])
@login_required
def add_order_item():
    """
        Add item order
        ---
        tags:
            - orders
        description: Add an item to the order in process of payment
        parameters:
            - in: header
              name: product_id
              description: The identification of the product that will be linked to the item of the order.
              type: integer
            - in: header
              name: quantity
              description: Quantity of the product to be purchased
              type: integer
            - in: header
              name: price
              description: Unit price of the product to be added to the order
              type: integer
        responses:
            200:
              description: The order item has been created
            400:
              description: The product had already been added to the cart
            500:
              description: Internal problem

    """
    product_id = request.form["product_id"]
    if get_order_item_by_product_id(product_id=product_id):
        cart_response = "Exist"
        response = HTTPStatus.BAD_REQUEST
    else:
        product_quantity = int(request.form["quantity"])
        user_id = current_user.id
        order_in = get_order_in_process_by_customer_id(customer_id=user_id)

        if order_in:
            order_id = order_in['id']
            product_price = int(request.form["price"])
            order_item_status_code = "OSI2"
            if create_order_item(product_id=product_id, order_id=order_id,
                                 order_item_status_code=order_item_status_code,
                                 order_item_quantity=product_quantity,
                                 order_item_price=(product_price * product_quantity)):
                cart_response = "Added"
                response = HTTPStatus.OK
            else:
                cart_response = "Fatal_Error"
                response = HTTPStatus.INTERNAL_SERVER_ERROR

        else:
            order_in = create_order(customer_id=user_id)

            order_id = order_in['id']
            product_price = int(request.form["price"])
            order_item_status_code = "OSI2"

            if create_order_item(product_id=product_id, order_id=order_id, order_item_status_code=order_item_status_code,
                                 order_item_quantity=product_quantity, order_item_price=(product_price*product_quantity)):
                cart_response = "Added"
                response = HTTPStatus.OK
            else:
                cart_response = "Fatal_Error"
                response = HTTPStatus.INTERNAL_SERVER_ERROR

    return redirect(url_for('store.show_product_view', product_id=product_id, cart_response=cart_response)), response


@order.route("/order-view", methods=["GET", "POST"])
@login_required
def show_order():
    if request.method == "POST":
        order_item_id = request.form["order_item_id"]
        if delete_order_item_by_id(order_item_id=order_item_id):
            return "Error"
    customer_id = current_user.id
    order_in = get_order_in_process_by_customer_id(customer_id=customer_id)
    if order_in:
        order_items = get_order_items_by_order_id(order_in["id"])
        if order_items:
            order_items_iva_prices = []
            order_subtotal_prices = []
            product_names = []
            total_price = 0
            for order_item in order_items:
                iva_price = (order_item["order_item_price"]*0.19)
                order_items_iva_prices.append(iva_price)
                subtotal_price = (iva_price+order_item["order_item_price"])
                total_price = total_price+subtotal_price
                order_subtotal_prices.append(subtotal_price)
                product = get_product_by_id(product_id=order_item["product_id"])
                product_name = product["name"]
                product_names.append(product_name)

            order_information = {"order_items": order_items, "order_items_iva_prices": order_items_iva_prices,
                                 "order_subtotal_prices": order_subtotal_prices, "product_names": product_names,
                                 "total_price": total_price}
            customer_payment_methods = get_customer_payment_methods_by_customer_id(customer_id=customer_id)
            ref_payment_methods = get_ref_payment_methods()


        else:
            order_information = {}
            customer_payment_methods = None
            ref_payment_methods = None
    else:
        order_information = {}
        ref_payment_methods = None
        customer_payment_methods = None

    return render_template("shopping-cart.html", order_information=order_information, pay=customer_payment_methods, refer=ref_payment_methods)


@order.route("/pay-order", methods=["POST"])
@login_required
def pay_order():
    """
       An order is paid
       ---
       tags:
           - orders
       description: An order payment is made and the invoice and payment are generated.
       parameters:
           - in: header
             name: payment-method-selection
             description: The card that the user selected for payment
             type: string
           - in: header
             name: payment_amount
             description: The total amount of the order
             type: integer
       responses:
           200:
             description: The order was paid and generated
           500:
             description: Could not update order
           500:
             description: The invoice could not be generated
           500:
             description: The payment could not be generated
       """
    credit_card_id = request.form["payment-method-selection"]
    payment_method = get_customer_payment_method_by_id(credit_card_id)
    payment_amount = request.form["payment_amount"]
    customer_id = current_user.id
    order_in = get_order_in_process_by_customer_id(customer_id=customer_id)
    invoice_status_code = "IS1"
    if payment_method["payment_method_code"] == "01A":
        invoice_details = "Factura pagada por Crédito"
    elif payment_method["payment_method_code"] == "02A":
        invoice_details = "Factura pagada por Débito"

    invoice = create_invoice(order_id=order_in["id"], invoice_status_code=invoice_status_code, invoice_details=invoice_details)
    if invoice:
        invoice_number = invoice.number
        payment = create_payment(invoice_number=invoice_number, payment_amount=payment_amount)
        if payment:
            if change_status_order_by_customer_id(customer_id=customer_id):
                message = "Error al actualizar la orden"
                response = HTTPStatus.INTERNAL_SERVER_ERROR
            else:
                message = "Se ha efectuado el pago exitosamente"
                response = HTTPStatus.OK
        else:
            message = "Ha ocurrido un error con el pago"
            response = HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        message = "Ha ocurrido un error con la factura"
        response = HTTPStatus.INTERNAL_SERVER_ERROR

    flash(message)
    return render_template("payment_result.html")














