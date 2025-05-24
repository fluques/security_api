from db import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

class UsersPermissionsModel(db.Model, UserMixin):
    __tablename__= "users_permissions"
    
    id =db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    permissions_id = db.Column(db.Integer, db.ForeignKey("permissions.id"))

    __table_args__ = (
        UniqueConstraint(user_id, permissions_id),
    )
    
    def __repr__(self):
        return f'<Users permissions {self.id}>'