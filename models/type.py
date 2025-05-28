from db import db
from flask_login import UserMixin
from sqlalchemy.event import listens_for
from sqlalchemy import event, text


class TypeModel(db.Model, UserMixin):
    __tablename__="types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship("UserModel", back_populates="types", secondary="users_types")




    def __repr__(self):
        return f'<Type {self.name}>'
    

@event.listens_for(TypeModel.__table__, "after_create")
def after_create(target, connection, **kw):
    connection.execute(
        text('INSERT INTO "types" ("id","name") VALUES (1, \'admin\');')
    )