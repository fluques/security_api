from db import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

class PermissionModel(db.Model, UserMixin):
    __tablename__= "permissions"
    
    id =db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    company = db.relationship("CompanyModel")
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"))
    resource = db.relationship("ResourceModel")
    action_id = db.Column(db.Integer, db.ForeignKey("actions.id"))
    action = db.relationship("ActionModel")
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"))
    application = db.relationship("ApplicationModel")
    users = db.relationship("UserModel", back_populates="permissions", secondary="users_permissions")
    groups = db.relationship("GroupModel", back_populates="permissions", secondary="groups_permissions")

    __table_args__ = (
        UniqueConstraint(company_id, resource_id, action_id, application_id),
    )