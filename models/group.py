from db import db
from flask_login import UserMixin
from sqlalchemy.event import listens_for


class GroupModel(db.Model, UserMixin):
    __tablename__="groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    is_active=db.Column(db.Boolean(),default=True)
    users = db.relationship("UserModel", back_populates="groups", secondary="groups_users")
    permissions = db.relationship("PermissionModel", back_populates="permissions", secondary="permissions_users")



    def __repr__(self):
        return f'<User {self.username}>'
    