from db import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint


class GroupsPermissionsModel(db.Model, UserMixin):
    __tablename__ = "groups_permissions"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    permissions_id = db.Column(db.Integer, db.ForeignKey("permissions.id"))

    __table_args__ = (
        UniqueConstraint(group_id, permissions_id),
    )
    

    def __repr__(self):
        return f'<Groups permissions {self.id}>'