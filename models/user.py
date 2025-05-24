from db import db
from flask_login import UserMixin


class UserModel(db.Model, UserMixin):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    groups = db.relationship("GroupModel", back_populates="users", secondary="groups_users")
    companies = db.relationship("CompanyModel", back_populates="users", secondary="companies_users")
    permissions = db.relationship("PermissionModel", back_populates="users", secondary="users_permissions")

    def __repr__(self):
        return f'<User {self.username}>'
    
