from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import GroupSchema,GroupUpdateSchema,UserSchema,UsersAndGroupsSchema
from models import GroupModel,UserModel, PermissionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from resources.permissions import PermissionValidate

blp = Blueprint("Groups", __name__, description="Operations on groups")


@blp.route("/group/<string:group_id>")
class Group(MethodView):
    @jwt_required()
    @blp.response(200, GroupSchema)
    def get(cls, group_id):
        if not PermissionValidate().get("/group/<string:group_id>", "GET"):
            abort(401,message=f'Authorization rejected for /group/<string:group_id>, action GET')

        group = GroupModel.query.get_or_404(group_id)
        return group

    @jwt_required()
    def delete(cls, group_id):
        if not PermissionValidate().get("/group/<string:group_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for /group/<string:group_id>, action DELETE')

        group = GroupModel.query.get_or_404(group_id)
        db.session.delete(group)
        db.session.commit()
        return {"message": "Group deleted."}

    @jwt_required()
    @blp.arguments(GroupUpdateSchema)
    @blp.response(200, GroupSchema)
    def put(self, group_data, group_id):
        if not PermissionValidate().get("/group/<string:group_id>", "PUT"):
            abort(401,message=f'Authorization rejected for /group/<string:group_id>, action PUT')

        group = GroupModel.query.get(group_id)

        if group:
            group.name = group_data["name"]
        else:
            group = GroupModel(id=group_id, **group_data)

        db.session.add(group)
        db.session.commit()

        return group


@blp.route("/group")
class GroupList(MethodView):
    @jwt_required()
    @blp.response(200, GroupSchema(many=True))
    def get(cls):
        if not PermissionValidate().get("/group", "GET"):
            abort(401,message=f'Authorization rejected for /group, action GET')

        return GroupModel.query.all()

    @jwt_required()
    @blp.arguments(GroupSchema)
    @blp.response(201, GroupSchema)
    def post(cls, group_data):
        if not PermissionValidate().get("/group", "POST"):
            abort(401,message=f'Authorization rejected for /group, action POST')

        group=GroupModel(**group_data)
        try:   
            db.session.add(group)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the group.")

        return group
    

@blp.route("/group/<int:group_id>/user/<int:user_id>")
class LinkUsersToGroup(MethodView):
    @jwt_required()
    @blp.response(201, GroupSchema)
    def post(self, group_id, user_id ):
        if not PermissionValidate().get("/group/<int:group_id>/user/<int:user_id>", "POST"):
            abort(401,message=f'Authorization rejected for /group/<int:group_id>/user/<int:user_id>, action POST')

        group = GroupModel.query.get_or_404(group_id)
        user = UserModel.query.get_or_404(user_id)
        group.users.append(user)

        try:
            db.session.add(group)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")

        return group

    @jwt_required()
    @blp.response(200, GroupSchema)
    def delete(self, group_id, user_id): 
        if not PermissionValidate().get("/group/<int:group_id>/user/<int:user_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for /group/<int:group_id>/user/<int:user_id>, action DELETE')

        group = GroupModel.query.get_or_404(group_id)
        user = UserModel.query.get_or_404(user_id)
        group.users.remove(user)

        try:
            db.session.add(group)
            db.session.commit()
            
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the user.")

        return {"message": "User removed from group", "group": group ,"user": user}






@blp.route("/group/<int:group_id>/permission/<int:permission_id>")
class LinkGroupsToUser(MethodView):
    @jwt_required()
    @blp.response(201, GroupSchema)
    def post(self, group_id, permission_id):
        if not PermissionValidate().get("/group/<int:group_id>/permission/<int:permission_id>", "POST"):
            abort(401,message=f'Authorization rejected for /group/<int:group_id>/permission/<int:permission_id>, action POST')

        group = GroupModel.query.get_or_404(group_id)
        permission = PermissionModel.query.get_or_404(permission_id)
        group.permissions.append(permission)

        try:
            db.session.add(group)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500, message="An error occurred while inserting the permission.")

        return group

    @jwt_required()
    @blp.response(200, GroupSchema)
    def delete(self, group_id, permission_id):
        if not PermissionValidate().get("/group/<int:group_id>/permission/<int:permission_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for /group/<int:group_id>/permission/<int:permission_id>, action DELETE')

        group = GroupModel.query.get_or_404(group_id)
        permission = PermissionModel.query.get_or_404(permission_id)
        group.permissions.remove(permission)

        try:
            db.session.add(group)
            db.session.commit()

        except SQLAlchemyError as ex:
            abort(500, message="An error occurred while removing the permission.")

        return group


