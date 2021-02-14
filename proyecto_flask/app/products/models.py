from datetime import datetime
from app.db import db, ma
from app.products.exceptions import ProductoNotFoundError


class Product(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), default="https://bit.ly/3loPYXP")
    price = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, default=1)
    description = db.Column(db.String(500), nullable=True)
    refundable = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "image", "refundable", "description"]


class Category(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


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


def get_all_categories():
    categories = Category.query.all()
    category_schema = CategorySchema()
    categories = [category_schema.dump(category) for category in categories]
    return categories


def create_new_category(name):
    category = Category(name=name)
    db.session.add(category)

    if db.session.commit():
        return category

    return None


def create_new_product(name, image, price, weight, description, refundable, category_id):

    category = Category.query.filter_by(id=category_id).first()

    if category:
        product = Product(name=name, image=image, price=price, weight=weight, description=description,
                          refundable=refundable, category_id=category_id)
        db.session.add(product)
        if db.session.commit():
            return product
    return None


def get_all_products():
    products_qs = Product.query.all()
    product_schema = ProductSchema()
    products_serialization = [product_schema.dump(product) for product in
                              products_qs]

    return products_serialization


def get_product_by_id(id):
    product_qs = Product.query.filter_by(id=id).first()
    if product_qs:
        product_schema = ProductSchema()
        p = product_schema.dump(product_qs)
        return p
    else:
        raise ProductoNotFoundError


def delete_product_by_id(id):
    Product.query.filter_by(id=id).delete()
    db.session.commit()


def create_stock_by_product(product_id, quantity):
    stock = Stock(product_id=product_id, quantity=quantity)
    db.session.add(stock)

    if db.session.commit():
        return stock

    return None


def get_stock_by_product(id):
    stock_qs = Stock.query.filter_by(id=id).first()
    stock_schema = StockSchema()
    s = stock_schema.dump(stock_qs)
    return s


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
