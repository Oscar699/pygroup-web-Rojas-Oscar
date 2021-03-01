from http import HTTPStatus

from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash

from app.admins.forms import CreateAdminForm
from app.admins.models import get_admin_by_email, create_admin_user

adminBp = Blueprint("adminBp", __name__, url_prefix="/admins")


@adminBp.route('/admin-panel/', methods=['GET'])
@login_required
def admin_panel():
    """
        Render the admin panel
        ---
        tags:
            - admins
        description: Shows a panel with all the options available to the admin
        responses:
            200:
              description: Rendered correctly
    """
    return render_template("admin-panel.html"), HTTPStatus.OK


@adminBp.route("/add-product", methods=["GET", "POST"])
@login_required
def create_product():
    """
        Render the new product form
        ---
        tags:
            - admins
        description: Show a form to add a new product to the database
        responses:
            200:
              description: Rendered correctly
    """
    return render_template("add-product-form.html"), HTTPStatus.OK


@adminBp.route("/add-category", methods=["GET", "POST"])
@login_required
def create_category():
    """
        Render the new category form
        ---
        tags:
            - admins
        description: Show a form to add a new category to the database
        responses:
            200:
              description: Rendered correctly
    """
    return render_template("add-category-form.html"), HTTPStatus.OK


@adminBp.route("/update-stock", methods=["GET", "POST"])
@login_required
def update_stock():
    """
        Render the new stock product form
        ---
        tags:
            - admins
        description: Show a form to add a new stock product to the database
        responses:
            200:
              description: Rendered correctly
    """
    return render_template("update-stock.html"), HTTPStatus.OK


@adminBp.route("/add-admin", methods=["GET", "POST"])
@login_required
def add_admin():
    form_admin = CreateAdminForm()
    if request.method == "POST" and form_admin.validate():
        admin_name = form_admin.admin_name.data
        email = form_admin.email.data
        password = form_admin.admin_password.data
        hash_password = generate_password_hash(password)

        if get_admin_by_email(email=email):
            flash("El correo ya esta siendo utilizado")
        else:
            if create_admin_user(admin_name=admin_name, admin_password=hash_password, email=email):
                flash("Admin creado correctamente")
            else:
                flash("Fallo al crear admin")

    return render_template("add-admin-form.html", form=form_admin), HTTPStatus.OK
