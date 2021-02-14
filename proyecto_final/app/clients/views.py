from flask import Blueprint, request, render_template
from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db
from app.clients.models import User
from app.clients.forms import CreateUserForm


from flask_login import login_user, logout_user, login_required

userBp = Blueprint("userBp", __name__, url_prefix="/user")


@userBp.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()
        password_validation = check_password_hash(user.password, password)
        if not user or not password_validation:
            flash("Revisa los datos ingrsados, algo anda mal :(")
            return redirect(url_for("userBp.login"))

        login_user(user)
        return redirect(url_for("store.home_page"))

    return render_template("login.html")


@userBp.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("store.home_page"))


@userBp.route("/signup/", methods=["GET", "POST"])
def signup():
    form_register = CreateUserForm()
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        login_name = request.form.get("login_name")
        password = request.form.get("password")
        address = request.form.get("address")
        phone_number = request.form.get("phone_number")

        user = User.query.filter_by(email=email,).first()

        if user:
            message = "User is already exist"
            flash(message)
            return redirect(url_for('userBp.signup'))

        hash_password = generate_password_hash(password)
        new_user = User(first_name=first_name, last_name=last_name, email=email,
                        login_name=login_name, password=hash_password, address=address, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        flash("Tu cuenta ha sido registrada. Inicia seision")
        return redirect(url_for('userBp.login'))

    return render_template('signup.html', form=form_register)