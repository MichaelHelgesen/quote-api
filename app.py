from flask import Flask, render_template, flash, request
from flask_smorest import abort

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
    person_id = StringField("Person ID", validators=[DataRequired()])
    quote = StringField("Quote", validators=[DataRequired()])
    source = StringField("Source")
    submit = SubmitField("Submit")

class UpdateQuoteForm(FlaskForm):
    quote_id = StringField("Quote ID", validators=[DataRequired()])
    quote = StringField("Quote", validators=[DataRequired()])
    source = StringField("Source")
    submit = SubmitField("Submit")

class DeleteForm(FlaskForm):
    person_id = StringField("Person ID", validators=[DataRequired()])
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

@app.get("/person")
def get_persons():
    return {"persons": list(persons.values())}

@app.post("/person")
def create_person():
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

@app.post("/quote")
def create_quote():
    quote_data = request.get_json()
    if ("quote" not in quote_data or "person_id" not in quote_data):
        abort(400, message="Bad request. Ensure 'quote' and 'person_id' are included in the JSON payload")
        
    if quote_data["person_id"] not in persons:
        abort(404, message = "Person not found")

    quote_id = uuid.uuid4().hex
    new_quote = {**quote_data, "id": quote_id}
    quotes[quote_id] = new_quote
    
    return new_quote, 201

@app.get("/quote")
def get_all_quotes():
    return {"quotes": list(quotes.values())}

@app.get("/person/<string:person_id>")
def get_person(person_id):
    try:
        return persons[person_id]
    except KeyError:
        abort(404, message = "Person not found")


@app.get("/quote/<string:quote_id>")
def get_quote(quote_id):
    try:
        return quotes[quote_id]
    except KeyError:
        abort(404, message = "Quote not found")

@app.delete("/quote/<string:quote_id>")
def delete_quote(quote_id):
    try:
        del quotes[quote_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message="Item not found")

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

@app.put("/quote/<string:quote_id>")
def update_quote(quote_id):
    quote_data = request.get_json()
    if "quote" not in quote_data or quote_data["quote"] == "":
        abort(400, message="Bad request. Ensure quote is written")

    try:
        quote = quotes[quote_id]
        quote |= quote_data

        return quote
    except KeyError:
        abort(404, message="Quote not found")

@app.route("/delete_person", methods=["GET", "POST"])
def del_person():
    person_id = None
    form = DeleteForm()
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

@app.delete("/person/<string:person_id>")
def delete_person(person_id):
    try:
        del persons[person_id]
        return {"message": "Person deleted"}
    except KeyError:
        abort(404, message="Person not found")
