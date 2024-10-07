from flask import request, render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import QuoteModel, TagModel, PersonModel 
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import QuoteSchema, QuoteUpdateSchema
from forms import QuoteForm


blp = Blueprint("Edit", __name__, description="Editing quotes")

@blp.route("/edit/<int:id>")
class EditQuote(MethodView):
    def get(self, id):
        #person_id = None
        quote = QuoteModel.query.get_or_404(id);
        person = PersonModel.query.get_or_404(quote.person.id)
        #source = None
        #tag = None
        form = QuoteForm()
        form.person_id.data = {person}
        test = TagModel.query.first()
        flash(test)
        form.tag.data = {test}
        flash(form.person_id.data) 
        #quotes = QuoteModel.query.all()
        persons = PersonModel.query.all()
        #tags = TagModel.query.all()
        form.tag.query = db.session.query(TagModel).order_by(TagModel.name)
        form.person_id.query = db.session.query(PersonModel).order_by(PersonModel.name)
        return render_template("update_quote.html",
            person_id = person.id,
            #tag = tag,
            quote = quote,
            #source = source,
            form = form,
            persons = persons,
            #tags = tags,
            #quotes = quotes
        )

    def post(self, id):
        #person_id = None
        quote = QuoteModel.query.get_or_404(id);
        #source = quote
        #tag = None
        form = QuoteForm()
        
        #quotes = QuoteModel.query.all()
        #persons = PersonModel.query.all()
        #tags = TagModel.query.all()
        form.person_id.query = db.session.query(PersonModel).order_by(PersonModel.name)
        flash("Update")
        flash(form.person_id.data)
        return render_template("update_quote.html",
            #person_id = person_id,
            #tag = tag,
            quote = quote,
            source = source,
            form = form,
            #persons = persons,
            #tags = tags,
            #quotes = quotes
        )
