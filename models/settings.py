from db import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import BYTEA

class SettingsModel(db.Model, UserMixin):
    __tablename__="settings"
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(BYTEA, nullable=True)

    def __repr__(self):
        return f'<Settings {self.id}>'