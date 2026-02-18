from flask import Response
from flask.views import MethodView, request
from flask_smorest import abort, Blueprint
from schemas import UserSchema, UserUpdateSchema,UserDetailSchema, GroupSchema,UsersAndGroupsSchema, UsersAndPermissionsSchema,PaginationSchema
from models import UserModel, GroupModel, PermissionModel
from db import db
from blocklist import BLOCKLIST
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from resources.permissions import PermissionValidate
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .odata_utils import apply_odata_query_with_pagination

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


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserDetailSchema)
    @jwt_required()
    def get(self, user_id):
        if not PermissionValidate().get("/user/<int:user_id>", "GET"):
            abort(401,message=f'Authorization rejected for resource /user/<int:user_id>, action GET')

        user = UserModel.query.options(joinedload(UserModel.groups),joinedload(UserModel.types),
                                       joinedload(UserModel.companies),joinedload(UserModel.permissions)).get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        if not PermissionValidate().get("/user/<int:user_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for resource /user/<int:user_id>, action DELETE')

        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}

    @jwt_required()
    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserDetailSchema)
    def put(self, user_data, user_id):
        if not PermissionValidate().get("/user/<int:user_id>", "PUT"):
            abort(401,message=f'Authorization rejected for resource /user/<int:user_id>, action PUT')
        
        user = UserModel.query.get(user_id)
        if user:
            user.user_name = user_data["user_name"]

            user.password= pbkdf2_sha256.hash(user_data["password"])
            user.email = user_data["email"]
            user.is_active = user_data["is_active"]
        else:
            user = UserModel(id=user_id, **user_data)

        db.session.add(user)
        db.session.commit()

        return user

@blp.route("/user")
class UserList(MethodView):
    @jwt_required()
    @blp.paginate() 
    @blp.response(200, UserSchema(many=True))
    def get(self,pagination_parameters):
        """Get a list of users with pagination
        """
        request_args = request.args.to_dict()

        if not PermissionValidate().get("/user", "GET"):
            abort(401,message=f'Authorization rejected for resource /user, action GET')

        pagination_parameters.item_count = 100
        order_by = request_args.get("$orderby", "")
        filter = request_args.get("$filter", "")

        orm_query = apply_odata_query_with_pagination((UserModel), filter, order_by, pagination_parameters)
        return orm_query.options(joinedload(UserModel.groups),joinedload(UserModel.types),joinedload(UserModel.companies)).all()

    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):

        if not PermissionValidate().get("/user", "POST"):
            abort(401,message=f'Authorization rejected for resource /user, action POST')

        user=UserModel(**user_data)
        try:
            user.password=pbkdf2_sha256.hash(user_data["password"])
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500,message="An error occurred while inserting the user.")

        return user


@blp.route("/user/<int:user_id>/group/<int:group_id>")
class LinkGroupsToUser(MethodView):
    @jwt_required()
    @blp.response(201, UserSchema)
    def post(self, user_id, group_id):

        if not PermissionValidate().get("/user/<int:user_id>/group/<int:group_id>", "POST"):
            abort(401,message=f'Authorization rejected for resource /user/<int:user_id>/group/<int:group_id>, action POST')

        user = UserModel.query.get_or_404(user_id)
        group = GroupModel.query.get_or_404(group_id)
        user.groups.append(group)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the group.")

        return user

    @jwt_required()
    @blp.response(200, UserSchema)
    def delete(self, user_id, group_id):

        if not PermissionValidate().get("/user/<int:user_id>/group/<int:group_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for resource /user/<int:user_id>/group/<int:group_id>, action DELETE')

        user = UserModel.query.get_or_404(user_id)
        group = GroupModel.query.get_or_404(group_id)
        user.groups.remove(group)
        try:
            db.session.add(user)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the group.")

        return {"message": "Group removed from user", "user": user, "group": group}
    


@blp.route("/user/<int:user_id>/permission/<int:permission_id>")
class LinkPermissionToUser(MethodView):
    @jwt_required()
    @blp.response(201, UserSchema)
    def post(self, user_id, permission_id):

        if not PermissionValidate().get("/user/<int:user_id>/permission/<int:permission_id>", "POST"):
            abort(401,message=f'Authorization rejected for resource /user/<int:user_id>/permission/<int:permission_id>, action POST')

        user = UserModel.query.get_or_404(user_id)
        permission = PermissionModel.query.get_or_404(permission_id)

        user.permissions.append(permission)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500, message="An error occurred while inserting the permission.")

        return user

    @jwt_required()
    @blp.response(200, UserSchema)
    def delete(self, user_id, permission_id):

        if not PermissionValidate().get("/user/<int:user_id>/permission/<int:permission_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for resource /user/<int:user_id>/permission/<int:permission_id>, action DELETE')

        user = UserModel.query.get_or_404(user_id)
        permission = PermissionModel.query.get_or_404(permission_id)
        user.permissions.remove(permission)

        try:
            db.session.add(user)
            db.session.commit()

        except SQLAlchemyError as ex:
            abort(500, message="An error occurred while removing the permission.")

        return user


