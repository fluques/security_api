from db import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

class PermissionsUsersModel(db.Model, UserMixin):
    __tablename__= "permissions_users"
    
    id =db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"))
    action_id = db.Column(db.Integer, db.ForeignKey("actions.id"))
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    __table_args__ = (
        UniqueConstraint(company_id, resource_id, action_id, application_id, user_id),
    )

    def __repr__(self):
        return f'<Permissions users {self.id}>'