from datetime import datetime

from flask import jsonify

from app.db import db, ma


class Product(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(500), default="Image")
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    refundable = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "image"]


class Category(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        fields = ["id", "name"]


class Stock(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stock
        fields = ["id", "product_id", "product_name","quantity"]


# Funcion que obtiene todos los productos
def get_all_products():
    products_qs = Product.query.all()
    product_schema = ProductSchema()
    products_serialization = [product_schema.dump(product) for product in
                              products_qs]

    return products_serialization


# Funcion que obtiene todos las categorias
def get_all_categories():
    categories = Category.query.all()
    category_schema = CategorySchema()
    categories = [category_schema.dump(category) for category in categories]
    return categories


# Funcion que obtiene el stock de un producto por su id
def get_stock_by_product(id):
    stock_qs = Stock.query.filter_by(id=id).first()
    stock_schema = StockSchema()
    s = stock_schema.dump(stock_qs)
    return s


# Crea un producto y lo sube a la bd
def create_new_product(name, image, price, weight, description, refundable, category_id):

    category = Category.query.filter_by(id=category_id).first()

    if category:
        product = Product(name=name, image=image, price=price, weight=weight, description=description,
                          refundable=refundable, category_id=category_id)
        db.session.add(product)
        if db.session.commit():
            return product
    return None


# Crea una categoria y la sube a la bd
def create_new_category(name):
    category = Category(name=name)
    db.session.add(category)

    if db.session.commit():
        return category

    return None


# Crea stock para un producto por su id
def create_stock_by_product(product_id, quantity):
    stock = Stock(product_id=product_id, quantity=quantity)
    db.session.add(stock)

    if db.session.commit():
        return stock

    return None


# Obtiene el stock de un producto
def get_stock_by_product(id):
    stock_qs = Stock.query.filter_by(id=id).first()
    stock_schema = StockSchema()
    s = stock_schema.dump(stock_qs)
    return s


# Actualiza el stock de un producto
def update_product_stock(id, new_quantity):
    product_stock = Stock.query.filter_by(id=id).first()
    if product_stock:
        product_stock.quantity += new_quantity
        db.session.commit()
        stock_schema = StockSchema()
        s = stock_schema.dump(product_stock)
        return s
    else:
        return None


