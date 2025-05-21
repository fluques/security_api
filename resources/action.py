from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ActionSchema
from models import ActionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("Actions", __name__, description="Operations on actions")


@jwt_required
@blp.route("/action/<string:action_id>")
class Action(MethodView):
    @blp.response(200, ActionSchema)
    def get(cls, action_id):
        action = ActionModel.query.get_or_404(action_id)
        return action

    def delete(cls, action_id):
        action = ActionModel.query.get_or_404(action_id)
        db.session.delete(action)
        db.session.commit()
        return {"message": "Action deleted."}

    @blp.arguments(ActionSchema)
    @blp.response(200, ActionSchema)
    def put(self, action_data, action_id):
        action = ActionModel.query.get(action_id)

        if action:
            action.name = action_data["name"]
        else:
            action = ActionModel(id=action_id, **action_data)

        db.session.add(action)
        db.session.commit()

        return action


@jwt_required
@blp.route("/action")
class ActionList(MethodView):
    @blp.response(200, ActionSchema(many=True))
    def get(cls):
        return ActionModel.query.all()

    @blp.arguments(ActionSchema)
    @blp.response(201, ActionSchema)
    def post(cls, action_data):
        action=ActionModel(**action_data)
        try:   
            db.session.add(action)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the action.")

        return action
    