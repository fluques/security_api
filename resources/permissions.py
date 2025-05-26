from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PermissionsSchema, PermissionsUpdateSchema, PlainPermissionsSchema
from models import PermissionModel, UserModel, UsersPermissionsModel, GroupModel, GroupsPermissionsModel, GroupsUsersModel, ResourceModel, ActionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity



blp = Blueprint("Permissions", __name__, description="Operations on permissions")



@blp.route("/permission/<string:permission_id>")
class Resource(MethodView):
    @jwt_required()
    @blp.response(200, PermissionsSchema)
    def get(cls, permission_id):
        permission = PermissionModel.query.get_or_404(permission_id)
        return permission

    @jwt_required()
    def delete(cls, permission_id):
        permission = PermissionModel.query.get_or_404(permission_id)
        db.session.delete(permission)
        db.session.commit()
        return {"message": "Permission deleted."}

    @jwt_required()
    @blp.arguments(PlainPermissionsSchema)
    @blp.response(200, PermissionsSchema)
    def put(self, permission_data, permission_id):
        permission = PermissionModel.query.get(permission_id)

        if permission:
            permission.company_id = permission_data["company_id"]
            permission.application_id = permission_data["application_id"]
            permission.resource_id = permission_data["resource_id"]
            permission.action_id = permission_data["action_id"]

        else:
            permission = PermissionModel(id=permission_id, **permission_data)

        db.session.add(permission)
        db.session.commit()

        return permission



@blp.route("/permission")
class ActionList(MethodView):
    @jwt_required()
    @blp.response(200, PermissionsSchema(many=True))
    def get(cls):
        return PermissionModel.query.all()

    @jwt_required()
    @blp.arguments(PlainPermissionsSchema)
    @blp.response(201, PermissionsSchema)
    def post(cls, permission_data):
        permission=PermissionModel(**permission_data)
        try:   
            db.session.add(permission)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the permission.")

        return permission
    

class PermissionValidate():
    def get(cls, resource_uri, action_name):
        current_user = get_jwt_identity()
        user = UserModel.query.get(current_user)
        action = ActionModel.query.where(ActionModel.name == action_name).first()
        resource = ResourceModel.query.where(ResourceModel.uri == resource_uri).first()
        
        user_permissions = UsersPermissionsModel.query.join(PermissionModel, (UsersPermissionsModel.permissions_id==PermissionModel.id) & (PermissionModel.action_id==action.id) & (PermissionModel.resource_id==resource.id) & (UsersPermissionsModel.user_id == user.id)).all()
        if len(user_permissions) >0:
            return True
        
        group_permissions = GroupsPermissionsModel.query.join(PermissionModel, (GroupsPermissionsModel.permissions_id==PermissionModel.id) & (PermissionModel.action_id==action.id) & (PermissionModel.resource_id==resource.id) & (GroupsPermissionsModel.group_id.in_([x.id for x in user.groups]))).all()
        if len(group_permissions):
            return True
        
        return False
        