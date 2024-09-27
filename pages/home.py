from flask import request, render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import QuoteModel, TagModel, PersonModel 
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import QuoteSchema, QuoteUpdateSchema
from forms import QuoteForm


blp = Blueprint("Homepage", __name__, description="Adding quotes")

@blp.route("/")
class AddQuote(MethodView):
    def get(self):
        person_id = None
        quote = None
        source = None
        tag = None
        form = QuoteForm()
        persons = PersonModel.query.all()
        tags = TagModel.query.all()
        form.person_id.choices = [(persons.id, persons.name.title()) for persons in persons]
        #form.person_id.process([])
        form.person_id.choices.insert(0,("", "Velg person"))
        #form.tag.choices = [(t.id, t.name.title()) for t in tags]
        form.tag.query = db.session.query(TagModel).order_by(TagModel.name)
        flash(form.tag.data)
        return render_template("add_quote.html",
            person_id = person_id,
            tag = tag,
            quote = quote,
            source = source,
            form = form,
            persons = persons,
            tags = tags
        )

    def post(self):
        person_id = None
        quote = None
        source = None
        tag = None
        form = QuoteForm()
        persons = PersonModel.query.all()
        tags = TagModel.query.all()
        form.person_id.choices = [(persons.id, persons.name.title()) for persons in persons]
        #form.person_id.process([])
        form.person_id.choices.insert(0,("", "Velg person"))
        #form.tag.query = TagModel.query.all()
        #form.tag.choices = [(t.id, t.name.title()) for t in tags]
        form.tag.query = db.session.query(TagModel).order_by(TagModel.name)
        if form.validate_on_submit():
            if QuoteModel.query.filter(QuoteModel.quote == form.data["quote"]).first():
                flash("Quote already exist")
                return render_template("add_quote.html",
                    person_id = person_id,
                    tag = tag,
                    quote = quote,
                    source = source,
                    form = form,
                    persons = persons,
                    tags = tags
                )
                
            quote = QuoteModel(**{"person_id":form.data["person_id"], "quote":form.data["quote"], "source":form.data["source"]})
            flash("validate")
            flash(form.tag.data)
            selected_tags = request.form.getlist("tag")
            for tag in selected_tags:
                try: 
                    quote.tags.append(TagModel.query.get_or_404(tag))
                    flash("yes")
                except:
                    flash(tag)
                    tag = TagModel(**{"name":tag})
                    db.session.add(tag)
                    db.session.commit()
                    #quote.tags.append(tag)

            try:
                #db.session.add(quote)
                #db.session.commit()
                flash("Quote added")
                form.person_id.data = ""
                form.quote.data = []
                form.source.data = ""
                return redirect(url_for("Homepage.AddQuote"))
            except SQLAlchemyError:
                flash("something went wrong")
                return render_template("add_quote.html",
                    person_id = person_id,
                    tag = tag,
                    quote = quote,
                    source = source,
                    form = form,
                    persons = persons,
                    tags = tags
                )
            
            '''
            quote = QuoteModel(**{"person_id":form.data["person_id"], "quote":form.data["quote"], "source":form.data["source"]})
            if TagModel.query.filter(TagModel.name == form.data["tag"]).first():
                flash("Tag exists")
                return render_template("add_quote.html",
                    person_id = person_id,
                    quote = quote,
                    source = source,
                    tag = tag,
                    form = form

                )
            elif QuoteModel.query.filter(QuoteModel.quote == form.data["quote"]).first():
                flash("Quote exists")
                return render_template("add_quote.html",
                    person_id = person_id,
                    quote = quote,
                    source = source,
                    tag = tag,
                    form = form
                )
            else:
                tag = TagModel(**{"name":form.data["tag"]})
                try:
                    db.session.add(quote)
                    db.session.add(tag)
                    db.session.commit()
                    flash("Quote added")
                    form.person_id.data = ""
                    form.quote.data = ""
                    form.tag.data = ""
                    form.source.data = ""
                except SQLAlchemyError:
                    flash("Something went wrong")
                    return render_template("add_quote.html",
                        person_id = person_id,
                        quote = quote,
                        source = source,
                        tag = tag,
                        form = form
                    )
                    '''
        #flash("not validate")
        #flash(request.form["person_id"])
        #flash(form.quote.data)
        #flash(form.tag.data)
        #flash(form.tag.choices)
        #flash(form.source.data)
        return render_template("add_quote.html",
            person_id = person_id,
            tag = tag,
            quote = quote,
            source = source,
            form = form,
            persons = persons,
            tags = tags
        )
