from app.db import db


class User(db.Model):
    id = db.Columnn(db.Integer, primary_key=True)
    email = db.Columnn(db.String(100), unique=True)
    password = db.Columnn(db.String(100))
    name = db.Columnn(db.String(250))