from db import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import BYTEA

class CompanySettingsModel(db.Model, UserMixin):
    __tablename__= "companies_settings"

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String, unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    #company = db.relationship("CompanyModel", back_populates="settings",  uselist=False)

    def __repr__(self):
        return f'<Company settings {self.id}>'