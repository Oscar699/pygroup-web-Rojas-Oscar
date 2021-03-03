from datetime import datetime
from app.db import db, ma
from app.orders.exceptions import InvoiceNotFoundError


class RefOrderStatusCode(db.Model):
    order_status_code = db.Column(db.String, primary_key=True)
    order_status_description = db.Column(db.String)


class RefOrderStatusCodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RefOrderStatusCode
        fields = ["order_status_code", "order_status_description"]


class Order(db.Model):
    """

    """
    id = db.Column(db.String, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_status_code = db.Column(db.String, db.ForeignKey(RefOrderStatusCode.order_status_code))
    date_created = db.Column(db.DateTime, default=datetime.now())
    order_details = db.Column(db.String)


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        fields = ["id", "customer_id", "order_status_code", "date_created", "order_details"]


class RefOrderItemStatusCode(db.Model):
    order_item_status_code = db.Column(db.String, primary_key=True)
    order_item_status_description = db.Column(db.String)


class RefOrderItemStatusCodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RefOrderItemStatusCode
        fields = ["order_status_code", "order_status_description"]


class OrderItem(db.Model):
    """

    """
    id = db.Column(db.String, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column(db.String, db.ForeignKey('order.id'))
    order_item_status_code = db.Column(db.String, db.ForeignKey(RefOrderItemStatusCode.order_item_status_code))
    order_item_quantity = db.Column(db.Integer, nullable=False)
    order_item_price = db.Column(db.Integer, nullable=False)
    other_order_item_details = db.Column(db.String)


class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "order_id", "order_status_code", "order_item_quantity", "order_item_price",
                  "other_order_item_details"]


class RefInvoiceStatusCode(db.Model):
    invoice_status_code = db.Column(db.String, primary_key=True)
    invoice_status_code_description = db.Column(db.String)


class RefInvoiceStatusCodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RefInvoiceStatusCode
        fields = ["invoice_status_code", "invoice_status_code_description"]


class Invoice(db.Model):
    number = db.Column(db.Numeric(4, 0), primary_key=True)
    order_id = db.Column(db.String, db.ForeignKey('order.id'))
    invoice_status_code = db.Column(db.String, db.ForeignKey(RefInvoiceStatusCode.invoice_status_code))
    invoice_date = db.Column(db.DateTime, default=datetime.now())
    invoice_details = db.Column(db.String)


class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    model = Invoice
    fields = ["number", "order_id", "invoice_status_code", "invoice_details"]


class Payment(db.Model):
    id = db.Column(db.Numeric(4, 0), primary_key=True)
    invoice_number = db.Column(db.Numeric, db.ForeignKey('invoice.number'))
    payment_date = db.Column(db.DateTime, default=datetime.now())
    payment_amount = db.Column(db.Integer, nullable=False)


class PaymentSchema(ma.SQLAlchemyAutoSchema):
    model = Payment
    fields = ["id", "invoice_number", "payment_date", "payment_amount"]


# Funcion que crea una orden en progreso de pago
def create_order(customer_id):
    if not Order.query.filter_by(customer_id=customer_id).first():
        id = "F0"
    else:
        n = len(Order.query.all())
        id = "F" + str(n + 1)

    status_code = "OS1"
    ref = RefOrderStatusCode.query.filter_by(order_status_code=status_code).first()
    details = ref.order_status_description
    order = Order(id=id, customer_id=customer_id, order_status_code=status_code, order_details=details)
    db.session.add(order)
    db.session.commit()
    order_in_process = get_order_in_process_by_customer_id(customer_id=customer_id)

    if order_in_process:
        return order_in_process
    else:
        return None


# Funcion que obtiene la orden en proceso de pago de un usuario
def get_order_in_process_by_customer_id(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    order_in_process = None
    for order in orders:
        if order.order_status_code == "OS1":
            order_in_process = order
            break

    if order_in_process:
        order_schema = OrderSchema()
        order_s = order_schema.dump(order_in_process)
        return order_s
    else:
        return None


# Cambia el status de una orden
def change_status_order_by_customer_id(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    order_in_process = None
    for order in orders:
        if order.order_status_code == "OS1":
            order_in_process = order
            break

    order_in_process.order_status_code = "OS2"
    order_in_process.order_details = "Pagada"
    db.session.commit()

    if get_order_in_process_by_customer_id(customer_id):
        return True
    else:
        return None


# Funcion que crea un item de orden
def create_order_item(product_id, order_id, order_item_status_code, order_item_quantity, order_item_price):
    ref = RefOrderItemStatusCode.query.filter_by(order_item_status_code=order_item_status_code).first()
    other_order_item_details = ref.order_item_status_description
    if not OrderItem.query.all():
        id = "OI0"
    else:
        n = len(OrderItem.query.all())
        id = "OI" + str(n + 1)
        if OrderItem.query.filter_by(id=id).first():
            id = "OI" + str(n + 2)
    order_item = OrderItem(id=id, product_id=product_id, order_id=order_id,
                           order_item_status_code=order_item_status_code,
                           order_item_quantity=order_item_quantity, order_item_price=order_item_price,
                           other_order_item_details=other_order_item_details)

    db.session.add(order_item)
    db.session.commit()

    if OrderItem.query.filter_by(product_id=product_id).first():
        return True
    else:
        return False


# Funcion que elimina un item de orden
def delete_order_item_by_id(order_item_id):
    order_item = OrderItem.query.filter_by(id=order_item_id).first()
    db.session.delete(order_item)
    db.session.commit()
    if OrderItem.query.filter_by(id=order_item_id).first():
        return "Error"
    else:
        return None


# Funcion que elimina los item de una orden por su id
def delete_order_items_by_order_id(order_id):
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    if order_items:
        for order_item in order_items:
            db.session.delete(order_item)
        db.session.commit()


# Obitnene los items de una orden por su producto
def get_order_item_by_product_id(product_id):
    order_item_qs = OrderItem.query.filter_by(product_id=product_id).first()
    if order_item_qs:
        order_item_schema = OrderItemSchema()
        order_item = order_item_schema.dump(order_item_qs)
        return order_item
    else:
        return None


# Funcion que obtiene todos los items de una orden
def get_order_items_by_order_id(order_id):
    order_items_qs = OrderItem.query.filter_by(order_id=order_id).all()
    if order_items_qs:
        order_items_schema = OrderItemSchema()
        order_items = [order_items_schema.dump(order_item) for order_item in
                       order_items_qs]
        return order_items
    else:
        return None


# Funcion que crea la factura correspondiente
def create_invoice(order_id, invoice_status_code, invoice_details):
    if not Invoice.query.all():
        number = 0
    else:
        n = len(Invoice.query.all())
        number = n + 1
        if Invoice.query.filter_by(number=number).first():
            number = n + 2
    invoice = Invoice(number=number, order_id=order_id, invoice_status_code=invoice_status_code,
                      invoice_details=invoice_details)
    db.session.add(invoice)
    db.session.commit()

    invoice_qs = Invoice.query.filter_by(order_id=order_id).first()
    if invoice_qs:
        invoice_schema = InvoiceSchema()
        print(invoice_schema)
        invoice = invoice_schema.dump(invoice_qs)
        print(invoice)
        return invoice_qs
    else:
        return None


# Funcion que elimina una factura por el id de la orden relacionada
def delete_invoice_by_order_id(order_id):
    invoice = Invoice.query.filter_by(order_id=order_id).first()
    if invoice:
        db.session.delete(invoice)
        db.session.commit()
        return True
    else:
        raise InvoiceNotFoundError
        return None


# Funcion que crea los pagos
def create_payment(invoice_number, payment_amount):
    if not Payment.query.all():
        id = 0
    else:
        n = len(Payment.query.all())
        id = n + 1
        if Payment.query.filter_by(id=id).first():
            id = n + 2
    payment = Payment(id=id, invoice_number=invoice_number, payment_amount=payment_amount)
    db.session.add(payment)
    db.session.commit()

    payment_qs = Payment.query.filter_by(invoice_number=invoice_number).first()
    if payment_qs:
        payment_schema = PaymentSchema()
        payment = payment_schema.dump(payment_qs)
        return payment_qs
    else:
        return None


# Funcion que obtiene todos los payments
def get_payments():
    payments_qs = Payment.query.all()
    if payments_qs:
        payments_schema = PaymentSchema()
        payments = [payments_schema.dump(payment) for payment in
                    payments_qs]
        return payments_qs
    else:
        return None


# Funcion que elimina un pago por el numero de factura relaacionada
def delete_payments_by_invoice_number(invoice_number):
    payment = Payment.query.filter_by(invoice_number=invoice_number).first()
    if payment:
        db.session.delete(payment)
        db.session.commit()
        return True
    else:
        return False


# Funcion que borra toda la data de ordenes del usuario
def delete_customer_order_data(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    validator = True
    for order in orders:
        order_id = order.id
        delete_order_items_by_order_id(order_id=order_id)
        if get_order_items_by_order_id(order_id):
            validator = False
            break;
        invoice = Invoice.query.filter_by(order_id=order_id).first()
        delete_payments_by_invoice_number(invoice_number=invoice.number)
        if Payment.query.filter_by(invoice_number=invoice.number).first():
            validator = False
            break;
        delete_invoice_by_order_id(order_id=order_id)
        if Invoice.query.filter_by(order_id=order_id).first():
            validator = False
            break;
        db.session.delete(order)
    db.session.commit()
    if Order.query.filter_by(customer_id=customer_id).first():
        validator = False
    return validator



