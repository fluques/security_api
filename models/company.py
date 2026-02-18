from db import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import BYTEA


class CompanyModel(db.Model, UserMixin):
    __tablename__="companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    street = db.Column(db.String(150), nullable=False)
    zip_code = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(150), nullable=False)
    main_email = db.Column(db.String(150), nullable=False)
    emails=db.Column(db.String(350),nullable=False) 
    phone = db.Column(db.String(150), nullable=False)
    celphone = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    users = db.relationship("UserModel", back_populates="companies", secondary="companies_users")
    #settings_id= db.Column(db.Integer, db.ForeignKey("companies_settings.id"))
    settings = db.relationship("CompanySettingsModel",  lazy='joined', uselist=False)


    def __repr__(self):
        return f'<Company {self.name}>'
    
