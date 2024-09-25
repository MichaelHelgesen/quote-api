from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class QuoteForm(FlaskForm):
    person_id = StringField("Person", validators=[DataRequired()])
    quote = TextAreaField("Quote", validators=[DataRequired()] )
    source = StringField("Source")
    tag = StringField("Tag")
    submit = SubmitField("Submit")

