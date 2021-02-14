from app.db import db, ma
from flask_login import UserMixin


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


class RefPaymentMethod(db.Model):
    payment_method_code = db.Column(db.String, primary_key=True)
    payment_method_description = db.Column(db.String)


class RefPaymentMethodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RefPaymentMethod
        fields = ["payment_method_code", "payment_method_description"]


class CustomerPaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ## payment_method_code = db.Column(db.String, db.ForeignKey('refpaymentmethod.payment_method_code'))
    credit_card_number = db.Column(db.String)
    payment_method_details = db.Column(db.String)


class CustomerPaymentMethodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerPaymentMethod
        fields = ["id", "credit_card_number"]