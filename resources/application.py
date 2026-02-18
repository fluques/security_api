from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ApplicationSchema, ApplicationUpdateSchema
from models import ApplicationModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from resources.permissions import PermissionValidate

blp = Blueprint("Applications", __name__, description="Operations on applications")


@blp.route("/application/<string:application_id>")
class Application(MethodView):
    @jwt_required()
    @blp.response(200, ApplicationSchema)
    def get(cls, application_id):
        if not PermissionValidate().get("/application/<string:application_id>", "GET"):
            abort(401,message=f'Authorization rejected for /application/<string:application_id>, action GET')

        application = ApplicationModel.query.get_or_404(application_id)
        return application 
          
    @jwt_required()
    def delete(cls, application_id):
        if not PermissionValidate().get("/application/<string:application_id>", "DELETE"):
            abort(401,message=f'Authorization rejected for /application/<string:application_id>, action DELETE')

        application = ApplicationModel.query.get_or_404(application_id)
        db.session.delete(application)
        db.session.commit()
        return {"message": "Application deleted."}
    
    @jwt_required()
    @blp.arguments(ApplicationUpdateSchema)
    @blp.response(200, ApplicationSchema)
    def put(cls, application_data, application_id):
        if not PermissionValidate().get("/application/<string:application_id>", "PUT"):
            abort(401,message=f'Authorization rejected for /application/<string:application_id>, action PUT')

        application = ApplicationModel.query.get(application_id)

        if application:
            application.name = application_data["name"]
        else:
            application = ApplicationModel(id=application_id, **application_data)

        db.session.add(application)
        db.session.commit()

        return application


@blp.route("/application")
class ApplicationList(MethodView):
    @jwt_required()
    @blp.response(200, ApplicationSchema(many= True))
    def get(cls):
        if not PermissionValidate().get("/application", "GET"):
            abort(401,message=f'Authorization rejected for /application, action GET')

        return ApplicationModel.query.all()
    
    @jwt_required()
    @blp.arguments(ApplicationSchema)
    @blp.response(201, ApplicationSchema)
    def post(cls, application_data):
        if not PermissionValidate().get("/application", "POST"):
            abort(401,message=f'Authorization rejected for /application, action POST')

        application = ApplicationModel(**application_data)
        try:   
            db.session.add(application)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the application.")

        return application