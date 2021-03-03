from datetime import datetime

from app.db import db, ma
from app.products.exceptions import ProductNotFoundError, StockNotFoundError


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
        fields = ["id", "name", "image", "price", "description", "refundable"]


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
        fields = ["id", "category_name"]


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
        fields = ["id", "product_id","quantity"]


# Funcion que obtiene todos los productos
def get_all_products():
    products_qs = Product.query.all()
    product_schema = ProductSchema()
    products_serialization = [product_schema.dump(product) for product in
                              products_qs]

    return products_serialization


# Funcion que obtiene todos los productos con su categoria en comun
def get_products_by_category(category_id):
    products_qs = Product.query.filter_by(category_id=category_id).all()
    product_schema = ProductSchema()
    products_serialization = [product_schema.dump(product) for product in
                              products_qs]
    return products_serialization


# Funcion para obtener un producto por su id
def get_product_by_id(product_id):
    product_qs = Product.query.filter_by(id=product_id).first()
    if product_qs:
        product_schema = ProductSchema()
        p = product_schema.dump(product_qs)
        return p
    else:
        raise ProductNotFoundError
        return None


# Funcion que obtiene todos las categorias
def get_all_categories():
    categories = Category.query.all()
    category_schema = CategorySchema()
    categories = [category_schema.dump(category) for category in categories]
    return categories


# Funcion que obtiene una categoria por su id
def get_category_by_id(category_id):
    category_qs = Category.query.filter_by(id=category_id).first()
    category_schema = CategorySchema()
    category = category_schema.dump(category_qs)
    return category


# Obtiene el stock de un producto
def get_stock_by_product_id(product_id):
    stock_qs = Stock.query.filter_by(product_id=product_id).first()
    if stock_qs:
        stock_schema = StockSchema()
        s = stock_schema.dump(stock_qs)
        return s
    else:
        raise StockNotFoundError
        return None


# Actualiza el stock de un producto
def update_product_stock(product_id, new_quantity):
    product_stock = Stock.query.filter_by(product_id=product_id).first()
    if product_stock:
        old_quantity = product_stock.quantity
        product_stock.quantity += new_quantity
        db.session.commit()
        product_stock = Stock.query.filter_by(product_id=product_id).first()
        if product_stock.quantity == new_quantity+old_quantity:
            return "Stock actualizado correctamente"
        else:
            return "Problema en la base de datos"
    else:
        return None


# Funcion que crea stock para un producto por su id
def create_stock_by_product(product_id, quantity):
    stock = Stock(product_id=product_id, quantity=quantity)
    db.session.add(stock)
    db.session.commit()

    if Stock.query.filter_by(product_id=product_id).first():
        return "Stock creado exitosamente"

    return "Fallo al crear el stock"


# Crea un producto y lo sube a la bd
def create_new_product(name, image, price, description, refundable, category_id):
    category = Category.query.filter_by(id=category_id).first()

    if category:
        product = Product(name=name, image=image, price=price, description=description,
                          refundable=refundable, category_id=category_id)
        db.session.add(product)
        db.session.commit()

        if Product.query.filter_by(name=product.name).first():
            return "Producto creado exitosamente"
        else:
            return "Fallo en la base de datos"
    else:
        return "La categoria no existe"


# Funcion que crea una categoria y la sube a la bd
def create_new_category(category_name):
    if Category.query.filter_by(category_name=category_name).first():
        return "Esta categoria ya existe"
    else:
        category = Category(category_name=category_name)
        db.session.add(category)
        db.session.commit()
        if Category.query.filter_by(category_name=category_name).first():
            return "Categoria creada exitosamente"
        else:
            return "Fallo en la base de datos"









