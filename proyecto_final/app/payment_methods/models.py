from app.db import db, ma


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
    payment_method_code = db.Column(db.String, db.ForeignKey(RefPaymentMethod.payment_method_code))
    credit_card_number = db.Column(db.String)
    payment_method_details = db.Column(db.String)


class CustomerPaymentMethodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerPaymentMethod
        fields = ["id", "credit_card_number", "payment_method_details", "payment_method_code"]


# Funcion para crear un metodo de pago de usuario
def create_customer_payment_method(customer_id, payment_method_code, credit_card_number, payment_method_details):
    customer_pay = CustomerPaymentMethod(customer_id=customer_id, payment_method_code=payment_method_code,
                                         credit_card_number=credit_card_number, payment_method_details=payment_method_details)
    db.session.add(customer_pay)
    db.session.commit()

    if CustomerPaymentMethod.query.filter_by(credit_card_number=customer_pay.credit_card_number):
        return True
    else:
        return False


# Funcion que obtiene todos los metodos de pago por id de usuario
def get_customer_payment_methods_by_customer_id(customer_id):
    customer_payment_methods_qs = CustomerPaymentMethod.query.filter_by(customer_id=customer_id).all()
    if customer_payment_methods_qs:
        customer_payment_methods_schema = CustomerPaymentMethodSchema()
        customer_payment_methods = [customer_payment_methods_schema.dump(customer_payment) for customer_payment in customer_payment_methods_qs]
        return customer_payment_methods
    else:
        return None


# Funcion que obtiene un metodo de pago por su id
def get_customer_payment_method_by_id(id):
    customer_payment_method_qs = CustomerPaymentMethod.query.filter_by(id=id).first()
    if customer_payment_method_qs:
        customer_payment_method_schema = CustomerPaymentMethodSchema()
        customer_payment_method = customer_payment_method_schema.dump(customer_payment_method_qs)
        return customer_payment_method
    else:
        return None


# Funcion para eliminar un metodo de pago de un usuario
def delete_customer_payment_method_by_id(id):
    payment_method = CustomerPaymentMethod.query.filter_by(id=id).first()

    db.session.delete(payment_method)
    db.session.commit()

    if not CustomerPaymentMethod.query.filter_by(id=id).first():
        return True
    else:
        return False


# Funcion para eliminar varios metodos de pago de usuario por id
def delete_customer_payments_methods(user_id):
    payments_methods = CustomerPaymentMethod.query.filter_by(customer_id=user_id).all()

    for payment_method in payments_methods:
        db.session.delete(payment_method)
        db.session.commit()

        print("Ref", CustomerPaymentMethod.query.filter_by(customer_id=user_id).all())

    if CustomerPaymentMethod.query.filter_by(customer_id=user_id).all():
        return False
    else:
        return True


# Funcion que obtiene todos los metodos de pago
def get_all_methods():
    methods_qs = RefPaymentMethod.query.all()
    methods_schema = RefPaymentMethodSchema()
    methods_serialization = [methods_schema.dump(product) for product in methods_qs]

    return methods_serialization


# Funcion que crea un nuevo metodo de pago
def add_payment_method(description, code):
    method = RefPaymentMethod(payment_method_description=description, payment_method_code=code)

    db.session.add(method)
    db.session.commit()

    if RefPaymentMethod.query.filter_by(payment_method_description=method.payment_method_description).first():
        return "El metodo de pago fue creado exitosamente"
    else:
        return "Fallo en la base de datos"


# Funcion que obtiene todas las referencias de metodos de pago
def get_ref_payment_methods():
    ref_pay_qs = RefPaymentMethod.query.all()
    if ref_pay_qs:
        ref_pay_schema = RefPaymentMethodSchema()
        ref_pay_methods = [ref_pay_schema.dump(ref_pay_method) for ref_pay_method in ref_pay_qs]
        return ref_pay_methods
    else:
        return None


