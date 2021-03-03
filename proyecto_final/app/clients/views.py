from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

from app.orders.models import get_payments, delete_customer_order_data
from app.payment_methods.models import (
    delete_customer_payments_methods,
    get_customer_payment_methods_by_customer_id,
    get_ref_payment_methods
)
from app.db import db
from app.clients.models import User
from app.admins.models import AdminUser
from app.clients.forms import (
    CreateUserForm,
    UpdatePhoneNumberForm,
    UpdateEmailForm,
    UpdateAddressForm,
    UpdatePasswordForm,
    UpdateFirstNameForm,
    UpdateLastNameForm,
    UpdateLoginNameForm,
)
from app.clients.models import (
    delete_customer,
    update_customer
)

from flask_login import current_user

from random import randint


from flask_login import login_user, logout_user, login_required

userBp = Blueprint("userBp", __name__, url_prefix="/user")


# vista para iniciar sesion
@userBp.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()
        if user:
            password_validation = check_password_hash(user.password, password)
        else:
            password_validation = ""
        if not user or not password_validation:
            adminUser = AdminUser.query.filter_by(email=email).first()
            if adminUser:
                password_admvalidation = check_password_hash(adminUser.admin_password, password)
            else:
                password_admvalidation = ""
            if not adminUser or not password_admvalidation:
                flash("Revisa los datos ingrsados, algo anda mal :(")
                return redirect(url_for("userBp.login"))

            login_user(adminUser)
            return redirect(url_for("adminBp.admin_panel"))

        login_user(user, remember=remember_me)
        return redirect(url_for("store.home_page"))

    return render_template("login.html")


@userBp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("store.home_page"))


# vista para registrarse
@userBp.route("/signup/", methods=["GET", "POST"])
def signup():
    form_register = CreateUserForm()
    if request.method == "POST" and form_register.validate():
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        login_name = request.form.get("login_name")
        password = request.form.get("password")
        address = request.form.get("address")
        phone_number = request.form.get("phone_number")

        user = User.query.filter_by(email=email).first()

        if user:
            message = "El correo ya esta en uso"
            flash(message)
            return redirect(url_for('userBp.signup'))
            response = HTTPStatus.BAD_REQUEST

        hash_password = generate_password_hash(password)
        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        login_name=login_name, password=hash_password, address=address, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        flash("Tu cuenta ha sido registrada. Inicia seision")
        response = HTTPStatus.ok
        return redirect(url_for('userBp.login'))
    else:
        response = HTTPStatus.BAD_REQUEST

    return render_template('signup.html', form=form_register), response


# vista para acceder a los datos de la cuenta y actualizar los datos personales
@userBp.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    form_first_name = UpdateFirstNameForm()
    form_last_name = UpdateLastNameForm()
    form_email = UpdateEmailForm()
    form_login_name = UpdateLoginNameForm()
    form_password = UpdatePasswordForm()
    form_address = UpdateAddressForm()
    form_phone = UpdatePhoneNumberForm()
    user_id = current_user.id
    payment_methods = get_customer_payment_methods_by_customer_id(customer_id=user_id)
    ref_pay_method = get_ref_payment_methods()
    payments = get_payments()

    forms = {"form_first_name": form_first_name, "form_last_name": form_last_name, "form_email": form_email,
             "form_login_name": form_login_name, "form_password": form_password, "form_address": form_address, "form_phone": form_phone}

    return render_template('cuenta.html', forms=forms, pay=payment_methods, refer=ref_pay_method, payments=payments)


# Vista para cambiar los datos personales}
@userBp.route("/cuenta/personal-data/<int:option>", methods=["POST"])
@login_required
def account_personal_data_update(option):
    """
        Updates personal data
        ---
        tags:
            - clients
        description: The data that the user wants to update of their personal data is collected
        parameters:
            - in: header
              name: first_name
              description: The new username
              type: string
            - in: header
              name: last_name
              description: The new lastname
              type: string
            - in: header
              name: email
              description: The new email
              type: string
            - in: header
              name: login_name
              description: The new username
              type: string
            - in: header
              name: password
              description: The new password
              type: string
            - in: header
              name: address
              description: The new address
              type: string
            - in: header
              name: phone_number
              description: The new phone_number
              type: integer
        responses:
            200:
              description: The user payment method has been deleted.
    """
    form_first_name = UpdateFirstNameForm()
    form_last_name = UpdateLastNameForm()
    form_email = UpdateEmailForm()
    form_login_name = UpdateLoginNameForm()
    form_password = UpdatePasswordForm()
    form_address = UpdateAddressForm()
    form_phone = UpdatePhoneNumberForm()
    user_id = current_user.id
    validator = False
    if option == 1:
        if form_first_name.validate():
            data = form_first_name.first_name.data
            validator = True
            flash("Nombre ctualizado correctamente")
    elif option == 2:
        if form_last_name.validate():
            data = form_last_name.last_name.data
            validator = True
            flash("Apellido actualizado correctamente")
    elif option == 3:
        if form_email.validate():
            data = form_email.email.data
            validator = True
            flash("Email atualizado correctamente")
    elif option == 4:
        if form_login_name.validate():
            data = form_login_name.login_name.data
            validator = True
            flash("Nombre de usuario ctualizado correctamente")
    elif option == 5:
        if form_password.validate():
            hash_password = generate_password_hash(form_password.password.data)
            data = hash_password
            validator = True
            flash("Contraseña actualizada correctamente")
    elif option == 6:
        if form_address.validate():
            data = form_address.address.data
            validator = True
            flash("Dirección actualizado correctamente")
    elif option == 7:
        if form_phone.validate():
            data = form_phone.phone_number.data
            validator = True
            flash("Número celular actualizado correctamente")
    if validator:
        update_customer(option=option, user_id=user_id, data=data)
    else:
        flash("¡Entrada invalida!", form_phone.errors)

    return redirect(url_for("userBp.account"))


# Vista que elimina toda la informacion de un usuario
@userBp.route("/delete-user-account", methods=["POST"])
@login_required
def account_delete():
    """
        Delete user account
        ---
        tags:
            - clients
        description: Delete the user's account and information related to it
        parameters:
            - in: session
              name: user_id
              description: The id of user account
              type: integer
        responses:
            200:
              description: The user payment method has been deleted.
            500:
               description: Internal server error.
    """
    user_id = current_user.id
    if delete_customer_order_data(customer_id=user_id) and delete_customer_payments_methods(user_id=user_id) and delete_customer(user_id=user_id):
        response = HTTPStatus.OK
    else:
        return "Error"
        response = HTTPStatus.INTERNAL_SERVER_ERROR
    return redirect(url_for("store.home_page"))



