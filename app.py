from flask import Flask, render_template, flash
from flask import request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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

persons = [
    {
        "name": "aristoteles",
        "quotes": [
            {
            "quote": "To be or not to be",
            "source": "Book"
            }
        ]
    }
]

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
    return {"persons": persons}

@app.post("/person")
def create_person():
    request_data = request.get_json()
    new_person = {"name": request_data["name"], "quotes": []}
    persons.append(new_person)
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

@app.post("/person/<string:name>/quote")
def create_quote(name):
    request_data = request.get_json()
    for person in persons:
        if person["name"] == name:
            new_quote = {"quote": request_data["quote"], "source": request_data["source"]}
            person["quotes"].append(new_quote)
            return new_quote, 201
    return {"message": "Person not found"}, 404
