from db import db
from flask_login import UserMixin

class ActionModel(db.Model, UserMixin):
    __tablename__="actions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<Action {self.name}>'
    