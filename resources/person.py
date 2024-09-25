import uuid
from flask import request, render_template, flash
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PersonSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import PersonModel
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PersonForm(FlaskForm):
    name = StringField("What name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class DeletePersonForm(FlaskForm):
    person_id = StringField("Person ID", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
blp = Blueprint("Persons", __name__, description="Operations on persons")

@blp.route("/person/<string:person_id>")
class Person(MethodView):
    @blp.response(200, PersonSchema)
    def get(self, person_id):
        person = PersonModel.query.get_or_404(person_id)
        return person

    def delete(self, person_id):
        person = PersonModel.query.get_or_404(person_id)
        db.session.delete(person)
        db.session.commit()
        return {"message": "Person deleted"}

@blp.route("/person")
class PersonList(MethodView):
    @blp.response(201, PersonSchema(many=True))
    def get(self):
        return PersonModel.query.all()
    
    @blp.arguments(PersonSchema)
    @blp.response(200, PersonSchema)
    def post(self, person_data):
        person = PersonModel(**person_data)
        
        try:
            db.session.add(person)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Person with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occured")

        return person, 201

@blp.route("/add_person", methods=["GET", "POST"])
def home():
    name = None
    form = PersonForm()
    if form.validate_on_submit():
        person = PersonModel(**{"name":form.data["name"]})
        try:
            db.session.add(person)
            db.session.commit()
            form.name.data = ""
            flash("Person added")
        except IntegrityError:
            flash("Person already exists")
            return render_template("add_person.html",
                name = name,
                form = form,
            )
        except SQLAlchemyError:
            flash("An error occured")
            return render_template("add_person.html",
                name = name,
                form = form,
            )

    return render_template("add_person.html",
        name = name,
        form = form,
    )

@blp.route("/delete_person", methods=["GET", "POST"])
def del_person():
    person_id = None
    form = DeletePersonForm()
    if form.validate_on_submit():
        person = PersonModel.query.get(form.person_id.data)
        try: 
            db.session.delete(person)
            db.session.commit()
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

