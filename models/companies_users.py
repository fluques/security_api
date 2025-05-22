from db import db
from sqlalchemy.schema import PrimaryKeyConstraint

class CompaniesUsers(db.Model):
    __tablename__ = "companies_users"

    group_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
 
    __table_args__ = (
        PrimaryKeyConstraint("group_id", "user_id"),
    )