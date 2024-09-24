from flask import Flask, render_template, flash
from flask_smorest import Api

from db import db
import models

from resources.quote import blp as QuoteBlueprint
from resources.person import blp as PersonBlueprint

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

    # Create a form class
    class PersonForm(FlaskForm):
        name = StringField("What name", validators=[DataRequired()])
        submit = SubmitField("Submit")

    class QuoteForm(FlaskForm):
        person_id = StringField("Person ID", validators=[DataRequired()])
        quote = StringField("Quote", validators=[DataRequired()])
        source = StringField("Source")
        submit = SubmitField("Submit")

    class UpdateQuoteForm(FlaskForm):
        quote_id = StringField("Quote ID", validators=[DataRequired()])
        quote = StringField("Quote", validators=[DataRequired()])
        source = StringField("Source")
        submit = SubmitField("Submit")

    class DeletePersonForm(FlaskForm):
        person_id = StringField("Person ID", validators=[DataRequired()])
        submit = SubmitField("Submit")

    class DeleteQuoteForm(FlaskForm):
        quote_id = StringField("Quote ID", validators=[DataRequired()])
        submit = SubmitField("Submit")

    @app.route("/add_person", methods=["GET", "POST"])
    def home():
        name =  None
        form = PersonForm()
        if form.validate_on_submit():
            name = form.name.data
            person_id = uuid.uuid4().hex
            new_person = {"name": name, "id": person_id}
            persons[person_id] = new_person
            form.name.data = ""
            flash("Person added")
        return render_template("add_person.html",
            name = name,
            form = form,
        )


    @app.route("/add_quote", methods=["GET", "POST"])
    def add_quote():
        person_id = None
        quote = None
        source = None
        form = QuoteForm()
        if form.validate_on_submit():
            person_id = form.person_id.data
            quote = form.quote.data
            source = form.source.data
            if person_id not in persons:
                flash("Name not found")
                return render_template("add_quote.html",
                    name = person_id,
                    quote = quote,
                    source = source,
                    form = form
                )

            quote_id = uuid.uuid4().hex
            new_quote = {"quote": quote, "source": source, "id": quote_id, "person_id": person_id}
            quotes[quote_id] = new_quote
            form.person_id.data = ""
            form.quote.data = ""
            form.source.data = ""
            flash("Quote added")
            return render_template("add_quote.html",
                person_id = person_id,
                quote = quote,
                source = source,
                form = form
            )
        return render_template("add_quote.html",
            person_id = person_id,
            quote = quote,
            source = source,
            form = form
        )

    @app.route("/update_quote", methods=["GET", "POST"])
    def upd_quote():
        quote_id = None
        quote = None
        source = None
        form = UpdateQuoteForm()
        if form.validate_on_submit():
            quote_id = form.quote_id.data
            source = form.source.data
            quote = form.quote.data
            if quote_id not in quotes:
                flash("Quote not found")
                return render_template("update_quote.html",
                    quote_id = quote_id,
                    quote = quote,
                    source = source,
                    form = form
                )

            new_quote = {"quote": quote, "source": source}
            original_quote = quotes[quote_id]
            original_quote |= new_quote
            form.quote_id.data = ""
            form.quote.data = ""
            form.source.data = ""
            flash("Quote updated")
            return render_template("update_quote.html",
                quote_id = quote_id,
                quote = quote,
                source = source,
                form = form
            )
        return render_template("update_quote.html",
            quote_id = quote_id,
            quote = quote,
            source = source,
            form = form
        )

    @app.route("/delete_person", methods=["GET", "POST"])
    def del_person():
        person_id = None
        form = DeletePersonForm()
        if form.validate_on_submit():
            person_id = form.person_id.data
            try: 
                del persons[person_id]
                form.person_id.data = ""
                flash("Person deleted")
                return render_template("delete_person.html",
                    person_id = person_id,
                    form = form
                )
            except:
                flash("Person not found")
                return render_template("delete_person.html",
                    person_id = person_id,
                    form = form
                )

        return render_template("delete_person.html",
            person_id = person_id,
            form = form
            )

    @app.route("/delete_quote", methods=["GET", "POST"])
    def del_quote():
        quote_id = None
        form = DeleteQuoteForm()
        if form.validate_on_submit():
            quote_id = form.quote_id.data
            try: 
                del quotes[quote_id]
                form.quote_id.data = ""
                flash("Quote deleted")
                return render_template("delete_quote.html",
                    quote_id = quote_id,
                    form = form
                )
            except:
                flash("Quote not found")
                return render_template("delete_quote.html",
                    quote_id = quote_id,
                    form = form
                )

        return render_template("delete_quote.html",
            quote_id = quote_id,
            form = form
            )
    return app

