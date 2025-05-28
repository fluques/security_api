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
        if not PermissionValidate().get("/permission/<string:permission_id>", "GET"):
            abort(401,message=f'Authorization rejected for resource /permission/<string:permission_id>, action PUT')

        permission = PermissionModel.query.get_or_404(permission_id)
        return permission

    @jwt_required()
    def delete(cls, permission_id):
        if not PermissionValidate().get("/permission/<string:permission_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for resource /permission/<string:permission_id>, action DELETE')

        permission = PermissionModel.query.get_or_404(permission_id)
        db.session.delete(permission)
        db.session.commit()
        return {"message": "Permission deleted."}

    @jwt_required()
    @blp.arguments(PlainPermissionsSchema)
    @blp.response(200, PermissionsSchema)
    def put(self, permission_data, permission_id):
        if not PermissionValidate().get("/permission/<string:permission_id>", "PUT"):
            abort(401,message=f'Authorization rejected for resource /permission/<string:permission_id>, action PUT')

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
        if not PermissionValidate().get("/permission", "GET"):
            abort(401,message=f'Authorization rejected for resource /permission, action GET')

        return PermissionModel.query.all()

    @jwt_required()
    @blp.arguments(PlainPermissionsSchema)
    @blp.response(201, PermissionsSchema)
    def post(cls, permission_data):
        if not PermissionValidate().get("/permission", "POST"):
            abort(401,message=f'Authorization rejected for resource /permission, action POST')

        permission=PermissionModel(**permission_data)
        try:   
            db.session.add(permission)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500,message="An error occurred while inserting the permission.")

        return permission
    

class PermissionValidate():
    def get(cls, resource_uri, action_name):
        current_user = get_jwt_identity()
        user = UserModel.query.get(current_user)
        action = ActionModel.query.where(ActionModel.name == action_name).first()
        resource = ResourceModel.query.where(ResourceModel.uri == resource_uri).first()

        #Check if is administrator
        if 1 in [x.id for x in user.groups] or user.id == 1:
            return True
        
        if not action or not resource:
            return False
        
        user_permissions = UsersPermissionsModel.query.join(PermissionModel, (UsersPermissionsModel.permissions_id==PermissionModel.id) & (PermissionModel.action_id==action.id) & (PermissionModel.resource_id==resource.id) & (UsersPermissionsModel.user_id == user.id)).all()
        if len(user_permissions) >0:
            return True
        
        group_permissions = GroupsPermissionsModel.query.join(PermissionModel, (GroupsPermissionsModel.permissions_id==PermissionModel.id) & (PermissionModel.action_id==action.id) & (PermissionModel.resource_id==resource.id) & (GroupsPermissionsModel.group_id.in_([x.id for x in user.groups]))).all()
        if len(group_permissions):
            return True
        
        return False
        