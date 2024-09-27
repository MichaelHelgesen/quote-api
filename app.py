from flask import Flask, render_template, flash
from flask_smorest import Api
from flask_bootstrap import Bootstrap4
from db import db
import models

from resources.quote import blp as QuoteBlueprint
from resources.person import blp as PersonBlueprint
from resources.tag import blp as TagBlueprint
from pages.home import blp as HomeBlueprint

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import uuid

import os
#from dotenv import load_dotenv
#load_dotenv()

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Sitat REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" 
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(QuoteBlueprint)
    api.register_blueprint(PersonBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(HomeBlueprint)
    bootstrap = Bootstrap4(app)
    return app

