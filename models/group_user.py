from db import db
from flask_login import UserMixin

class GroupsUsersModel(db.Model, UserMixin):
    __tablename__ = "groups_users"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def __repr__(self):
        return f'<Group users {self.id}>'