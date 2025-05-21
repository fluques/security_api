from db import db
from flask_login import UserMixin
from sqlalchemy.event import listens_for


class ResourceModel(db.Model, UserMixin):
    __tablename__="resources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<Resource {self.name}>'
    