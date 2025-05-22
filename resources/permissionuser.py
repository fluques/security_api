from flask.views import MethodView
from db import db
from flask_smorest import Blueprint, abort
from schemas import PermissionsAndUsersSchema
from models import PermissionsUsersModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("PermissionsUsers", __name__, description ="Operations on permissions users")

@blp.route("/permission-user/<string:permission_user_id>")
class PermissionUser(MethodView):
    @blp.response(200, PermissionsAndUsersSchema)
    def get(cls, permission_user_id):
        permission_user = PermissionsUsersModel.query.get_or_404(permission_user_id)
        return permission_user

    def delete(cls, permission_user_id):
        permission_user = PermissionsUsersModel.query.get_or_404(permission_user_id)
        db.session.delete(permission_user)
        db.session.commit()
        return {"message": "Permission user deleted."}

    @blp.arguments(PermissionsAndUsersSchema)
    @blp.response(200, PermissionsAndUsersSchema)
    def put(self, permission_user_data, permission_user_id):
        permission_user = PermissionsUsersModel.query.get(permission_user_id)

        if permission_user:
            permission_user.company_id = permission_user_data["company_id"]
            permission_user.resource_id = permission_user_data["resource_id"]
            permission_user.action_id = permission_user_data["action_id"]
            permission_user.application_id = permission_user_data["application_id"]
            permission_user.user_id = permission_user_data["user_id"]
        else:
            permission_user = PermissionsUsersModel(id=permission_user_id, **permission_user_data)

        db.session.add(permission_user)
        db.session.commit()

        return permission_user


@jwt_required
@blp.route("/permission-user")
class PermissionUserList(MethodView):
    @blp.response(200, PermissionsAndUsersSchema(many=True))
    def get(cls):
        return PermissionsUsersModel.query.all()

    @blp.arguments(PermissionsAndUsersSchema)
    @blp.response(201, PermissionsAndUsersSchema)
    def post(cls, permission_user_data):
        permission_user=PermissionsUsersModel(**permission_user_data)
        try:   
            db.session.add(permission_user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the permission user.")

        return permission_user
    

        

