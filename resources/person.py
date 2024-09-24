import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import persons
from schemas import PersonSchema

blp = Blueprint("Persons", __name__, description="Operations on persons")

@blp.route("/person/<string:person_id>")
class Person(MethodView):
    @blp.response(200, PersonSchema)
    def get(self, person_id):
        try:
            return persons[person_id]
        except KeyError:
            abort(404, message = "Person not found")

    def delete(self, person_id):
        try:
            del persons[person_id]
            return {"message": "Person deleted"}
        except KeyError:
            abort(404, message="Person not found")

@blp.route("/person")
class PersonList(MethodView):
    @blp.response(201, PersonSchema(many=True))
    def get(self):
        return persons.values()
    
    @blp.arguments(PersonSchema)
    @blp.response(200, PersonSchema)
    def post(self, person_data):
        for person in persons.values():
            if person_data["name"] == person["name"]:
                abort(400, message="Person already exists.")

        person_id = uuid.uuid4().hex
        new_person = {**person_data, "id": person_id}
        persons[person_id] = new_person

        return new_person, 201
