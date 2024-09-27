from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from models import TagModel
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

def get_tags_name():
      return TagModel.query

class QuoteForm(FlaskForm):

    person_id = SelectField("Person", validators=[DataRequired()])
    quote = TextAreaField("Quote", validators=[DataRequired()] )
    source = StringField("Source")
    tag = QuerySelectMultipleField("TAGS", get_label="name", allow_blank=False, blank_text="Select", render_kw={"size": 10})
    submit = SubmitField("Submit")

