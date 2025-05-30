from db import db
from flask_login import UserMixin
from sqlalchemy import event, insert, text
from passlib.hash import pbkdf2_sha256

class UserModel(db.Model, UserMixin):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    groups = db.relationship("GroupModel", back_populates="users", secondary="groups_users", lazy='noload')
    companies = db.relationship("CompanyModel", back_populates="users", secondary="companies_users", lazy='noload')
    permissions = db.relationship("PermissionModel", back_populates="users", secondary="users_permissions", lazy='noload')
    types = db.relationship("TypeModel", back_populates="users", secondary="users_types", lazy='noload')

    def __repr__(self):
        return f'<User {self.username}>'
    
stmt = insert(UserModel.__table__).values(id=1, usern_name="admin", email='ing.fernando@gmail.com', password='admin', is_active=True)

@event.listens_for(UserModel.__table__, "after_create")
def after_create(target, connection, **kw):
    connection.execute(
        text('INSERT INTO "public"."users" ("user_name", "email", "password", "is_active") VALUES (\'admin\', \'ing.fernando@gmail.com\', \''+ pbkdf2_sha256.hash("admin")+'\', True);')
    )

