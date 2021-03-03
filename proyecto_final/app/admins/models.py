from app.db import db, ma
from flask_login import UserMixin


class AdminUser(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    admin_name = db.Column(db.String(20), unique=True)
    admin_password = db.Column(db.String(50))
    email = db.Column(db.String(50))


class AdminUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdminUser
        fields = ["id", "admin_name"]


# Funcion que crea un admin
def create_admin_user(admin_name, admin_password, email):
    admin_qs = AdminUser.query.filter_by(email=email).all()
    if admin_qs:
        n = len(admin_qs)
        id = "adm" + str(n)
        if AdminUser.query.filter_by(id=id).first():
            id = "adm" + 2
    else:
        id = "adm0"

    admin = AdminUser(id=id, admin_name=admin_name, admin_password=admin_password, email=email)
    db.session.add(admin)
    db.session.commit()
    if AdminUser.query.filter_by(email=email).first():
        return admin
    else:
        return None


# Funcion que busca un admin por su email
def get_admin_by_email(email):
    admin_qs = AdminUser.query.filter_by(email=email).first()
    if admin_qs:
        admin_schema = AdminUserSchema()
        admin = admin_schema.dump(admin_qs)
        return admin
    else:
        return None