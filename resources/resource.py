from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ResourceSchema, ResourceUpdateSchema
from models import ResourceModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from resources.permissions import PermissionValidate

blp = Blueprint("Resources", __name__, description="Operations on resources")



@blp.route("/resource/<string:resource_id>")
class Resource(MethodView):
    @jwt_required()
    @blp.response(200, ResourceSchema)
    def get(cls, resource_id):
        if not PermissionValidate().get("/resource/<string:resource_id>", "GET"):
            abort(401,message=f'Authorization rejected for resource /resource/<string:resource_id>, action GET')

        resource = ResourceModel.query.get_or_404(resource_id)
        return resource

    @jwt_required()
    def delete(cls, resource_id):
        if not PermissionValidate().get("/resource/<string:resource_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for resource /resource/<string:resource_id>, action DELETE')

        resource = ResourceModel.query.get_or_404(resource_id)
        db.session.delete(resource)
        db.session.commit()
        return {"message": "Resource deleted."}

    @jwt_required()
    @blp.arguments(ResourceUpdateSchema)
    @blp.response(200, ResourceSchema)
    def put(self, action_data, resource_id):
        if not PermissionValidate().get("/resource/<string:resource_id>", "PUT"):
            abort(401,message=f'Authorization rejected for resource /resource/<string:resource_id>, action PUT')

        resource = ResourceModel.query.get(resource_id)

        if resource:
            resource.name = action_data["name"]
            resource.uri = action_data["uri"]
        else:
            resource = ResourceModel(id=resource_id, **action_data)

        db.session.add(resource)
        db.session.commit()

        return resource



@blp.route("/resource")
class ActionList(MethodView):
    @jwt_required()
    @blp.response(200, ResourceSchema(many=True))
    def get(cls):
        if not PermissionValidate().get("/resource", "GET"):
            abort(401,message=f'Authorization rejected for resource /resource, action GET')
        return ResourceModel.query.all()

    @jwt_required()
    @blp.arguments(ResourceSchema)
    @blp.response(201, ResourceSchema)
    def post(cls, action_data):
        if not PermissionValidate().get("/resource", "POST"):
            abort(401,message=f'Authorization rejected for resource /resource, action POST')

        action=ResourceModel(**action_data)
        try:   
            db.session.add(action)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the action.")

        return action
    