from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import CompanyModel
from schemas import CompanySchema, CompanyUpdateSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required


blp = Blueprint("Comapanies", __name__, description ="Operations on applications")

@jwt_required
@blp.route("/company/string:company_id")
class Company(MethodView):
    @blp.response(200, CompanySchema)
    def get(cls, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        return company

    def delete(cls, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        db.session.delete(company)
        db.session.commit()
        return {"message": "Company deleted."}
    

    @blp.arguments(CompanyUpdateSchema)
    @blp.response(200, CompanySchema)
    def put(cls, company_data, company_id):
        company = CompanyModel.query.get(company_id)

        if company:
            company.name = company_data["name"]
            company.street = company_data["street"]
            company.zip_code = company_data["zip_code"]
            company.city = company_data["city"]
            company.state = company_data["state"]
            company.country = company_data["country"]
            company.main_email = company_data["main_email"]
            company.emails = company_data["emails"]
            company.phone = company_data["phone"]
            company.celphone = company_data["celphone"]
            company.is_active = company_data["is_active"]

        else:
            company = CompanyModel(id=company_id, **company_data)

        db.session.add(company)
        db.session.commit()

        return company


@jwt_required
@blp.route("/company")
class CompanyList(MethodView):
    @blp.response(200, CompanySchema(many=True))
    def get(cls):
        return CompanyModel.query.all()
    def post(cls, company_data):
        company = CompanyModel(**company_data)
        try:   
            db.session.add(company)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the company.")

        return company