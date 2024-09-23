from flask import Flask, render_template, flash
from flask import request

from db import persons, quotes

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import uuid

import os
#from dotenv import load_dotenv
#load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Create a form class
class PersonForm(FlaskForm):
    name = StringField("What name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class QuoteForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    quote = StringField("Quote", validators=[DataRequired()])
    source = StringField("Source")
    submit = SubmitField("Submit")


@app.route("/add_person", methods=["GET", "POST"])
def home():
    name =  None
    form = PersonForm()
    if form.validate_on_submit():
        name = form.name.data
        new_person = {"name": form.name.data, "quotes": []}
        persons.append(new_person)
        form.name.data = ""
        flash("Person added")
    return render_template("add_person.html",
        name = name,
        form = form,
    )

@app.get("/person")
def get_persons():
    return {"persons": list(persons.values())}

@app.post("/person")
def create_person():
    person_data = request.get_json()
    person_id = uuid.uuid4().hex
    new_person = {**person_data, "id": person_id}
    persons[person_id] = new_person
    return new_person, 201


@app.route("/add_quote", methods=["GET", "POST"])
def add_quote():
    name = None
    quote = None
    source = None
    form = QuoteForm()
    if form.validate_on_submit():
        name = form.name.data
        quote = form.quote.data
        source = form.source.data
        for person in persons:
            if person["name"] == name:
                new_quote = {"quote": form.quote.data, "source": form.source.data}
                person["quotes"].append(new_quote)
                form.name.data = ""
                form.quote.data = ""
                form.source.data = ""
                flash("Quote added")
                return render_template("add_quote.html",
                    name = name,
                    quote = quote,
                    source = source,
                    form = form
                )
        flash("Name not found")

    return render_template("add_quote.html",
        name = name,
        quote = quote,
        source = source,
        form = form
    )

@app.post("/quote")
def create_quote():
    quote_data = request.get_json()
    if item_data["person_id"] not in persons:
        return {"message": "Person not found"}, 404

    quote_id = uuid.uuid4().hex
    new_quote = {**quote_data, "id": quote_id}
    quotes[quote_id] = new_quote
    
    return {"message": "Person not found"}, 404

@app.get("/quote")
def get_all_quotes():
    return {"quotes": list(quotes.values())}

@app.get("/person/<string:person_id>")
def get_person(person_id):
    try:
        return persons[person_id]
    except KeyError:
        return {"message": "Person not found"}, 404


@app.get("/quote/<string:quote_id>")
def get_quote(quote_id):
    try:
        return quotes[quote_id]
    except KeyError:
        return {"message": "Quote not found"}, 404
