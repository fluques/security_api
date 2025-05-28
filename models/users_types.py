from sqlalchemy import UniqueConstraint
from db import db
from flask_login import UserMixin
from sqlalchemy import event, text

class UsersTypesModel(db.Model, UserMixin):
    __tablename__ = "users_types"

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey("types.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    __table_args__ = (
        UniqueConstraint(type_id, user_id),
    )

    def __repr__(self):
        return f'<Types users {self.id}>'
    
@event.listens_for(UsersTypesModel.__table__, "after_create")
def after_create(target, connection, **kw):
    connection.execute(
        text('INSERT INTO "users_types" ("id","type_id","user_id") VALUES (1, 1, 1);')
    )