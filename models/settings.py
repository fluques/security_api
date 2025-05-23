from db import db
from flask_login import UserMixin


class SettingsModel(db.Model, UserMixin):
    __tablename__="settings"
    id = db.Column(db.Integer, primary_key=True)
    smtp_server = db.Column(db.String, nullable=True)
    smtp_user = db.Column(db.String, nullable=True)
    smtp_password = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Settings {self.id}>'