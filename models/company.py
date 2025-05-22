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
    emails=db.Column(db.String(350),unique=True,nullable=False) 
    phone = db.Column(db.String(150), nullable=False)
    celphone = db.Column(db.String(150), nullable=False)
    logo = db.Column(BYTEA, nullable=True)
    is_active = db.Column(db.Boolean(), default=True)
    users = db.relationship("UserModel", back_populates="users", secondary="companies_users")


    def __repr__(self):
        return f'<Company {self.name}>'
    
