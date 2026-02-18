from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import SettingsSchema
from models import SettingsModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from resources.permissions import PermissionValidate

blp = Blueprint("Settings", __name__, description="Operations on settings")


@blp.route("/settings/<string:settings_id>")
class Settings(MethodView):
    @jwt_required()
    @blp.response(200, SettingsSchema)
    def get(cls, settings_id):
        if not PermissionValidate().get("/settings/<string:settings_id>", "GET"):
            abort(401,message=f'Authorization rejected for resource /settings/<string:settings_id>, action GET')

        settings = SettingsModel.query.get_or_404(settings_id)
        return settings
    
    @jwt_required()
    def delete(cls, settings_id):
        if not PermissionValidate().get("/settings/<string:settings_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for resource /settings/<string:settings_id>, action DELETE')

        settings = SettingsModel.query.get_or_404(settings_id)
        db.session.delete(settings)
        db.session.commit()
        return {"message": "Settings deleted."}
    
    @jwt_required()
    @blp.arguments(SettingsSchema)
    @blp.response(200, SettingsSchema)
    def put(self, settings_data, settings_id):
        if not PermissionValidate().get("/settings/<string:settings_id>", "PUT"):
            abort(401,message=f'Authorization rejected for resource /settings/<string:settings_id>, action PUT')

        settings = SettingsModel.query.get(settings_id)

        if settings:
            settings.smtp_server = settings_data["smtp_server"]
            settings.smtp_user = settings_data["smtp_user"]
            settings.smtp_password = settings_data["smtp_password"]

        else:
            settings = SettingsModel(id=settings_id, **settings_data)

        db.session.add(settings)
        db.session.commit()

        return settings


@blp.route("/settings")
class SettingsList(MethodView):
    @jwt_required()
    @blp.response(200, SettingsSchema(many=True))
    def get(cls):
        if not PermissionValidate().get("/settings", "GET"):
            abort(401,message=f'Authorization rejected for resource /settings, action GET')
        return SettingsModel.query.all()
    
    @jwt_required()
    @blp.arguments(SettingsSchema)
    @blp.response(201, SettingsSchema)
    def post(cls, settings_data):
        if not PermissionValidate().get("/settings", "POST"):
            abort(401,message=f'Authorization rejected for resource /settings, action POST')

        settings=SettingsModel(**settings_data)
        try:   
            db.session.add(settings)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the settings.")

        return settings
    