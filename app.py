from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import request
import os
#from dotenv import load_dotenv
#load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Create a form class
class PersonForm(FlaskForm):
    name = StringField("What name", validators=[DataRequired()])
    submit = SubmitField("Submit")

persons = [
    {
        "name": "Aristoteles",
        "quotes": [
            {
            "quote": "To be or not to be",
            "Source": "Book"
            }
        ]
    }
]

@app.route("/", methods=["GET", "POST"])
def home():
    name =  None
    form = PersonForm()
    if form.validate_on_submit():
        name = form.name.data
        new_person = {"name": form.name.data, "quotes": []}
        persons.append(new_person)
        form.name.data = ""
    return render_template("index.html",
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

