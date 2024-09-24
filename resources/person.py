import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import persons

blp = Blueprint("Persons", __name__, description="Operations on persons")

@blp.route("/person/<string:person_id>")
class Person(MethodView):
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
    def get(self):
        return {"persons": list(persons.values())}
    
    def post(self):
        person_data = request.get_json()

        if "name" not in person_data or person_data["name"] == "":
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload")

        for person in persons.values():
            if person_data["name"] == person["name"]:
                abort(400, message="Person already exists.")

        person_id = uuid.uuid4().hex
        new_person = {**person_data, "id": person_id}
        persons[person_id] = new_person

        return new_person, 201
