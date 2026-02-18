from db import db
from sqlalchemy.schema import  UniqueConstraint

class CompaniesUsers(db.Model):
    __tablename__ = "companies_users"

    id = db.Column(db.Integer, primary_key= True)
    group_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
 
    __table_args__ = (
        UniqueConstraint("group_id", "user_id"),
    )

    def __repr__(self):
        return f'<Companies users {self.id}>'