from flask.views import MethodView
from db import db
from flask_smorest import Blueprint, abort
from schemas import PermissionsAndUsersSchema, PermissionsAndGroupsSchema
from models import PermissionsUsersModel, PermissionsGroupsModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("PermissionsGroups", __name__, description ="Operations on permissions groups")

@blp.route("/permission-group/<string:permission_group_id>")
class PermissionGroup(MethodView):
    @blp.response(200, PermissionsAndGroupsSchema)
    def get(cls, permission_group_id):
        permission_group = PermissionsGroupsModel.query.get_or_404(permission_group_id)
        return permission_group

    def delete(cls, permission_group_id):
        permission_group = PermissionsGroupsModel.query.get_or_404(permission_group_id)
        db.session.delete(permission_group)
        db.session.commit()
        return {"message": "Permission group deleted."}

    @blp.arguments(PermissionsAndGroupsSchema)
    @blp.response(200, PermissionsAndGroupsSchema)
    def put(self, permission_group_data, permission_group_id):
        permission_group = PermissionsGroupsModel.query.get(permission_group_id)

        if permission_group:
            permission_group.company_id = permission_group_data["company_id"]
            permission_group.resource_id = permission_group_data["resource_id"]
            permission_group.action_id = permission_group_data["action_id"]
            permission_group.application_id = permission_group_data["application_id"]
            permission_group.group_id = permission_group_data["group_id"]
        else:
            permission_group = PermissionsGroupsModel(id=permission_group_id, **permission_group_data)

        db.session.add(permission_group)
        db.session.commit()

        return permission_group


@jwt_required
@blp.route("/permission-group")
class PermissionGroupList(MethodView):
    @blp.response(200, PermissionsAndGroupsSchema(many=True))
    def get(cls):
        return PermissionsGroupsModel.query.all()

    @blp.arguments(PermissionsAndGroupsSchema)
    @blp.response(201, PermissionsAndGroupsSchema)
    def post(cls, permission_group_data):
        permission_group=PermissionsGroupsModel(**permission_group_data)
        try:   
            db.session.add(permission_group)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the permission group.")

        return permission_group
    

        

