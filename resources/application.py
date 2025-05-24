from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ApplicationSchema, ApplicationUpdateSchema
from models import ApplicationModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("Applications", __name__, description="Operations on applications")

@jwt_required
@blp.route("/application/<string:application_id>")
class Application(MethodView):
    @blp.response(200, ApplicationSchema)
    def get(cls, application_id):
        application = ApplicationModel.query.get_or_404(application_id)
        return application 
          
    def delete(cls, application_id):
        application = ApplicationModel.query.get_or_404(application_id)
        db.session.delete(application)
        db.session.commit()
        return {"message": "Application deleted."}
    
    @blp.arguments(ApplicationUpdateSchema)
    @blp.response(200, ApplicationSchema)
    def put(cls, application_data, application_id):
        application = ApplicationModel.query.get(application_id)

        if application:
            application.name = application_data["name"]
        else:
            application = ApplicationModel(id=application_id, **application_data)

        db.session.add(application)
        db.session.commit()

        return application

@jwt_required
@blp.route("/application")
class ApplicationList(MethodView):
    @blp.response(200, ApplicationSchema(many= True))
    def get(cls):
        return ApplicationModel.query.all()
    
    @blp.arguments(ApplicationSchema)
    @blp.response(201, ApplicationSchema)
    def post(cls, application_data):
        application = ApplicationModel(**application_data)
        try:   
            db.session.add(application)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the application.")

        return application