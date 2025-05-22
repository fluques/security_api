from db import db
from flask_login import UserMixin

class ApplicationModel(db.Model, UserMixin):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)