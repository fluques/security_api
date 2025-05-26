from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ActionSchema, ActionUpdateSchema
from models import ActionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from resources.permissions import PermissionValidate

blp = Blueprint("Actions", __name__, description="Operations on actions")



@blp.route("/action/<string:action_id>")
class Action(MethodView):
    @jwt_required()
    @blp.response(200, ActionSchema)
    def get(cls, action_id):
        if not PermissionValidate().get("/action/<string:action_id>", "GET"):
            abort(401,message=f'Authorization rejected for /action/<string:action_id>, action GET')

        action = ActionModel.query.get_or_404(action_id)
        return action

    @jwt_required()
    def delete(cls, action_id):
        if not PermissionValidate().get("/action/<string:action_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for /action/<string:action_id>, action DELETE')

        action = ActionModel.query.get_or_404(action_id)
        db.session.delete(action)
        db.session.commit()
        return {"message": "Action deleted."}

    @jwt_required()
    @blp.arguments(ActionUpdateSchema)
    @blp.response(200, ActionSchema)
    def put(self, action_data, action_id):
        if not PermissionValidate().get("/action/<string:action_id>", "PUT"):
            abort(401,message=f'Authorization rejected for /action/<string:action_id>, action PUT')

        action = ActionModel.query.get(action_id)

        if action:
            action.name = action_data["name"]
        else:
            action = ActionModel(id=action_id, **action_data)

        db.session.add(action)
        db.session.commit()

        return action



@blp.route("/action")
class ActionList(MethodView):
    @jwt_required()
    @blp.response(200, ActionSchema(many=True))
    def get(cls):
        if not PermissionValidate().get("/action", "GET"):
            abort(401,message=f'Authorization rejected for /action, action GET')

        return ActionModel.query.all()

    @jwt_required()
    @blp.arguments(ActionSchema)
    @blp.response(201, ActionSchema)
    def post(cls, action_data):
        if not PermissionValidate().get("/action", "POST"):
            abort(401,message=f'Authorization rejected for /action, action POST')

        action=ActionModel(**action_data)
        try:   
            db.session.add(action)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the action.")

        return action
    

    