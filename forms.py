from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired
from models import TagModel
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

def get_tags_name():
      return TagModel.query

class QuoteForm(FlaskForm):
    person_id = QuerySelectMultipleField("PERSON", get_label="name", allow_blank=False, blank_text="Select person", render_kw={"size": 30}, validators=[InputRequired()])
    quote = TextAreaField("Quote", validators=[InputRequired()] )
    source = StringField("Source")
    tag = QuerySelectMultipleField("TAGS", get_label="name", allow_blank=False, blank_text="Select", render_kw={"size": 10})
    submit = SubmitField("Submit")

class PersonForm(FlaskForm):
    name = StringField("What name", validators=[DataRequired()])
    submit = SubmitField("Submit")
