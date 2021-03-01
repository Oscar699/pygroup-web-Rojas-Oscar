from app.db import db, ma
from flask_login import UserMixin
from app.payment_methods.models import RefPaymentMethod, RefPaymentMethodSchema


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String(50), unique=True)
    login_name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))
    address = db.Column(db.String)
    phone_number = db.Column(db.Integer, unique=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ["id", "login_name", "email"]


# Funcion que actualiza los datos personales de un usuario
def update_customer(option, user_id, data):
    user = User.query.filter_by(id=user_id).first()
    if option == 1:
        user.first_name = data
    elif option == 2:
        user.last_name = data
    elif option == 3:
        user.email = data
    elif option == 4:
        user.login_name = data
    elif option == 5:
        user.password = data
    elif option == 6:
        user.address = data
    elif option == 7:
        user.phone_number = data
    db.session.commit()


# Funcion para eliminar un usuario
def delete_customer(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    if User.query.filter_by(id=user_id).first():
        return False
    else:
        return True


