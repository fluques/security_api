from sqlalchemy import UniqueConstraint
from db import db
from flask_login import UserMixin
from sqlalchemy import event, text

class GroupsUsersModel(db.Model, UserMixin):
    __tablename__ = "groups_users"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    __table_args__ = (
        UniqueConstraint(group_id, user_id),
    )

    def __repr__(self):
        return f'<Group users {self.id}>'
    
@event.listens_for(GroupsUsersModel.__table__, "after_create")
def after_create(target, connection, **kw):
    connection.execute(
        text('INSERT INTO "groups_users" ("id","group_id","user_id") VALUES (1, 1, 1);')
    )