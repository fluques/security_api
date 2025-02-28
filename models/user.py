from db import db
from flask_login import UserMixin
from sqlalchemy.event import listens_for


class UserModel(db.Model, UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    groups = db.relationship("GroupModel", back_populates="users", secondary="groups_users")

   # cart = db.Column(db.JSON, nullable=True, default=list)  # Make cart nullable

    # Define the relationship between User and CartProducts
    
    #cart_products = relationship('CartProducts', backref="user", lazy="dynamic")
    # Define the relationship between User and Wishlists
    #wishlists = db.relationship('Wishlists', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
'''@listens_for(User.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(User(id=1,username='admin',password="abc123",is_active=True))
    db.session.commit()'''