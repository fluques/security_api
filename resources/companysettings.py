from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CompanySchema, CompanyUpdateSchema, CompanySettingsSchema
from models import CompanySettingsModel, CompanyModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("CompanySettings", __name__, description="Operations on Company settings")


@jwt_required
@blp.route("/company/<string:company_id>/settings")
class CompanySettingsList(MethodView):
    @blp.response(200, CompanySchema)
    def get(cls, company_id):
        return CompanyModel.query.get_or_404(company_id)
    
    
    def delete(cls, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        db.session.delete(company.settings)
        db.session.commit()
        return {"message": "Company settings deleted."}


    @blp.arguments(CompanySettingsSchema)
    @blp.response(201, CompanySchema)
    def post(cls,  settings_data, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        company.settings = CompanySettingsModel(**settings_data)

        
        try:   
            db.session.add(company)
            db.session.commit()
        except SQLAlchemyError as ex:
            abort(500,message="An error occurred while inserting the company settings.")

        return company
    
    @blp.arguments(CompanySettingsSchema)
    @blp.response(200, CompanySchema)
    def put(self, settings_data, company_id):
        company = CompanyModel.query.get(company_id)

        if company.settings:
            company.settings.hostname = settings_data["hostname"]
        else:
            company.settings = CompanySettingsModel(**settings_data)

        db.session.add(company)
        db.session.commit()

        return company