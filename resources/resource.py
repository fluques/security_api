from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ResourceSchema
from models import ResourceModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("Resources", __name__, description="Operations on resources")


@jwt_required
@blp.route("/resource/<string:action_id>")
class Resource(MethodView):
    @blp.response(200, ResourceSchema)
    def get(cls, resource_id):
        resource = ResourceSchema.query.get_or_404(resource_id)
        return resource

    def delete(cls, resource_id):
        resource = ResourceModel.query.get_or_404(resource_id)
        db.session.delete(resource)
        db.session.commit()
        return {"message": "Resource deleted."}

    @blp.arguments(ResourceSchema)
    @blp.response(200, ResourceSchema)
    def put(self, action_data, resource_id):
        resource = ResourceModel.query.get(resource_id)

        if resource:
            resource.name = action_data["name"]
        else:
            resource = ResourceModel(id=resource_id, **action_data)

        db.session.add(resource)
        db.session.commit()

        return resource


@jwt_required
@blp.route("/action")
class ActionList(MethodView):
    @blp.response(200, ResourceSchema(many=True))
    def get(cls):
        return ResourceModel.query.all()

    @blp.arguments(ResourceSchema)
    @blp.response(201, ResourceSchema)
    def post(cls, action_data):
        action=ResourceModel(**action_data)
        try:   
            db.session.add(action)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the action.")

        return action
    