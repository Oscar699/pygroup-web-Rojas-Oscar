from flask import Blueprint, request, render_template
from app.db import db


auth = Blueprint("auth", __name__, url_prefix="")


@auth.route("/login")
def login():
    pass


@auth.route("/logout")
def logout():
    pass


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")

        user = User.query.filter_by(email=email).first()

        if user:
            message = "User have been created"
            flash(message)
            return redirect(url_for('auth.signup'))

        hash_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('signup.html')
