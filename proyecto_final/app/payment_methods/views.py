from random import randint
from flask_login import current_user, login_required
from flask import Blueprint, render_template, url_for, redirect, request, flash
from app.payment_methods.forms import CreatePaymentForm, CreateUserPayMethodForm
from app.payment_methods.models import add_payment_method, create_customer_payment_method, delete_customer_payment_method_by_id

paymentMethods = Blueprint("paymentMethods", __name__, url_prefix="/payment-methods")


@paymentMethods.route("/add-payment-methods/", methods=['GET', 'POST'])
@login_required
def create_payment_method():
    form_pay = CreatePaymentForm()
    message = ""
    if request.method == "POST" and form_pay.validate():
        print(form_pay.payment_code.data, "++", form_pay.payment_description.data)
        message = add_payment_method(description=form_pay.payment_description.data,
                                     code=form_pay.payment_code.data)

    return render_template("add-pay-methods.html", message=message, form=form_pay)


# Vista para agregar metodo de pago de usuario
@paymentMethods.route("/add-user-payment-method", methods=["GET", "POST"])
@login_required
def create_customer_pay():
    form_customer_pay = CreateUserPayMethodForm()
    if request.method == "POST" and form_customer_pay.validate():
        value = randint(1, 2)
        if value == 1:
            details = "En funcionamiento"
        else:
            details = "Sobregirada"

        if create_customer_payment_method(customer_id=current_user.id,
                                          payment_method_code=form_customer_pay.payment_method_code.data,
                                          credit_card_number=form_customer_pay.credit_card_number.data,
                                          payment_method_details=details):
            flash("Metodo creado satisfactoriamente")
        else:
            flash("Fallo en la base de datos")

    return render_template("add-customer-pay-method.html", form=form_customer_pay)


# Vista para eliminar metodos de pago de usuario
@paymentMethods.route("/delete-user-payment-method", methods=["POST"])
@login_required
def delete_customer_payment_method():
    """
        Delete user payment methods
        ---
        tags:
            - payment methods
        description: Remove the user's payment method by the given id
        parameters:
            - in: header
              name: payment_id
              description: The id of the id of the user's payment method
              type: integer
        responses:
            200:
              description: The user payment method has been deleted.
    """
    payment_id = int(request.form["payment_id"])
    delete_customer_payment_method_by_id(id=payment_id)
    return redirect(url_for("userBp.account"))
