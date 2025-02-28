from flask import Flask, jsonify
from flask_smorest import abort,Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from db import db
import models
from flask_migrate import Migrate
from resources.user import blp as UserBlueprint
from resources.group import blp as GroupBlueprint
import os



def create_app(db_url=None):
    app=Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Security REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL") or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate = Migrate(app, db)    
    api = Api(app)
    
    #This has to be one time in  the app 
    app.config["JWT_SECRET_KEY"] = "282709050867448692071479427955105377284"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # TODO: Read from a config file instead of hard-coding
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failedc2.", "error": "invalid_token"}
            ),
            401,
        )


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )


    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token is not fresh.", "error": "fresh_token_required"}
            ),
            401,
        )


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )




    #@app.get("/")
    def HelloName():
        return "Hello World 2!"

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(GroupBlueprint)

    return app




