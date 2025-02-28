from db import db

class GroupsUsers(db.Model):
    __tablename__ = "groups_users"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
