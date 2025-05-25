from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CompanySettingsSchema
from models import CompanySettingsModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("CompanySettings", __name__, description="Operations on Company settings")



@blp.route("/company/<string:company_id>/settings")
class aompanySettings(MethodView):
    @jwt_required()
    @blp.response(200, CompanySettingsSchema)
    def get(cls, company_id):
        settings = CompanySettingsModel.query.get_or_404(company_id)
        return settings
    
    @jwt_required()
    def delete(cls, company_id):
        settings = CompanySettingsModel.query.get_or_404(company_id)
        db.session.delete(settings)
        db.session.commit()
        return {"message": "Company settings deleted."}

    @jwt_required()
    @blp.arguments(CompanySettingsSchema)
    @blp.response(200, CompanySettingsSchema)
    def put(self, settings_data, company_id):
        settings = CompanySettingsModel.query.get(company_id)

        if settings:
            settings.smtp_server = settings_data["smtp_server"]
            settings.smtp_user = settings_data["smtp_user"]
            settings.smtp_password = settings_data["smtp_password"]

        else:
            settings = CompanySettingsModel(id=company_id, **settings_data)

        db.session.add(settings)
        db.session.commit()

        return settings


