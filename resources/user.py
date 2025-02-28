from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema, UserUpdateSchema,GroupSchema,UsersAndGroupsSchema
from models import UserModel, GroupModel
from db import db
from blocklist import BLOCKLIST
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.user_name == user_data["user_name"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

@jwt_required
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get(user_id)

        if user:
            user.user_name = user_data["user_name"]
            user.password = user_data["password"]
            user.email = user_data["email"]
            user.is_active = user_data["is_active"]
        else:
            user = UserModel(id=user_id, **user_data)

        db.session.add(user)
        db.session.commit()

        return user

@jwt_required
@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user=UserModel(**user_data)
        try:
            user.password=pbkdf2_sha256.hash(user_data["password"])
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the user.")

        return user

@jwt_required
@blp.route("/user/<int:user_id>/group/<int:group_id>")
class LinkGroupsToUser(MethodView):
    @blp.response(201, GroupSchema)
    def post(self, user_id, group_id):
        user = UserModel.query.get_or_404(user_id)
        group = GroupModel.query.get_or_404(group_id)

        user.groups.append(group)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the group.")

        return user

    @blp.response(200, UsersAndGroupsSchema)
    def delete(self, user_id, group_id):
        user = UserModel.query.get_or_404(user_id)
        group = GroupModel.query.get_or_404(group_id)

        user.groups.remove(group)

        try:
            db.session.add(user)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the group.")

        return {"message": "Group removed from user", "user": user, "group": group}


