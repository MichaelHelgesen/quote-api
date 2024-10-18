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
        source = quote.source
        #tag = None
        form = QuoteForm()
        form.person_id.data = {person}
        form.tag.data = quote.tags
        form.source.data = source
        form.quote.data = quote.quote
        #quotes = QuoteModel.query.all()
        #tags = TagModel.query.all()
        form.tag.query = db.session.query(TagModel).order_by(TagModel.name)
        form.person_id.query = db.session.query(PersonModel).order_by(PersonModel.name)
        return render_template("update_quote.html",
            person_id = person.id,
            #tag = tag,
            quote = quote,
            #source = source,
            form = form,
            #tags = tags,
            #quotes = quotes
        )

    def post(self, id):
        quote = QuoteModel.query.get_or_404(id);
        person_id = None
        #quote = None
        #source = None
        #tag = None
        #person = PersonModel.query.get_or_404(quote.person.id)
        form = QuoteForm()
        #form.quote.data = 
        flash("post")
        #flash(form.quote.data)
        
        form.tag.query = db.session.query(TagModel).order_by(TagModel.name)
        form.person_id.query = db.session.query(PersonModel).order_by(PersonModel.name)
        #quote.source = form.source.data
        selected_tags = request.form.getlist("tag")
        selected_persons = request.form.getlist("person_id")
        #flash(selected_tags)
        #flash(selected_persons)

        if form.validate_on_submit():
            
            for person in selected_persons:
                if PersonModel.query.get(person):
                    person_id = PersonModel.query.get(person).id
                    flash("Person is")
                else:
                    try: 
                        newPerson = PersonModel(**{"name":person})
                        flash("new person")
                        #db.session.add(newPerson)
                        #db.session.commit()
                        #person_id = PersonModel.query.filter(PersonModel.name == person).first().id
                    except:
                        #db.session.rollback()
                        flash("fd")

            for tag in quote.tags:
                if str(tag.id) not in selected_tags:
                    flash("-")
                    quote.tags.remove(TagModel.query.get(tag.id))
                    #flash("yes")
                else:
                    flash("-o")

            for tag in selected_tags:
                flash(tag)

            try:
                flash("try")
                #db.session.commit()
            except:
                flash("error")
            
            
            return redirect(url_for("Edit.EditQuote", id=id))
            '''
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
            '''
        flash("not validate")
        #return redirect(url_for("Edit.EditQuote", id=id))
        return render_template("update_quote.html",
            #person_id = person.id,
            #tag = tag,
            quote = quote,
            #source = source,
            form = form,
            #tags = tags,
            #quotes = quotes
            id = id
        )
