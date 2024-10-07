from flask import request, render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import QuoteModel, TagModel, PersonModel 
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import QuoteSchema, QuoteUpdateSchema
from forms import QuoteForm


blp = Blueprint("Homepage", __name__, description="Adding quotes")

@blp.route("/del_tag/<int:id>")
class RemoveTag(MethodView):
    def post(self, id):
        try:
            tag = TagModel.query.get_or_404(id)
            if not tag.quote:
                db.session.delete(tag)
                db.session.commit()
                flash("message: Tag deleted")
                return redirect(url_for('Homepage.AddQuote'))
        except:
            flash("ikke tag")
            return redirect(url_for('Homepage.AddQuote'))

@blp.route("/")
class AddQuote(MethodView):
    def get(self):
        person_id = None
        quote = None
        source = None
        tag = None
        form = QuoteForm()
        quotes = QuoteModel.query.all()
        persons = PersonModel.query.all()
        tags = TagModel.query.all()
        #form.person_id.choices = [(persons.id, persons.name.title()) for persons in persons]
        #form.person_id.process([])
        #form.person_id.choices.insert(0,("", "Velg person"))
        #form.tag.choices = [(t.id, t.name.title()) for t in tags]
        form.tag.query = db.session.query(TagModel).order_by(TagModel.name)
        form.person_id.query = db.session.query(PersonModel).order_by(PersonModel.name)
        #flash(form.tag.data)
        return render_template("add_quote.html",
            person_id = person_id,
            tag = tag,
            quote = quote,
            source = source,
            form = form,
            persons = persons,
            tags = tags,
            quotes = quotes
        )

    def post(self):
        person_id = None
        quote = None
        source = None
        tag = None
        form = QuoteForm()
        persons = PersonModel.query.all()
        quotes = QuoteModel.query.all()
        tags = TagModel.query.all()
        #form.person_id.choices = [(persons.id, persons.name.title()) for persons in persons]
        #form.person_id.process([])
        #form.person_id.choices.insert(0,("", "Velg person"))
        #form.tag.query = TagModel.query.all()
        #form.tag.choices = [(t.id, t.name.title()) for t in tags]
        form.tag.query = db.session.query(TagModel).order_by(TagModel.name)
        form.person_id.query = db.session.query(PersonModel).order_by(PersonModel.name)

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
                    tags = tags,
                    quotes = quotes
                )
            flash("validate")
            #flash(form.tag.data)
            selected_tags = request.form.getlist("tag")
            selected_persons = request.form.getlist("person_id")
            for person in selected_persons:
                if PersonModel.query.get(person):
                    person_id = PersonModel.query.get(person).id
                    flash("Person is")
                else:
                    try: 
                        newPerson = PersonModel(**{"name":person})
                        flash("testing")
                        db.session.add(newPerson)
                        db.session.commit()
                        person_id = PersonModel.query.filter(PersonModel.name == person).first().id
                        flash(person_id)
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close()
                        #form.person_id = person
                        #form.person_id.process()

            quote = QuoteModel(**{"person_id":person_id, "quote":form.data["quote"], "source":form.data["source"]})
            for tag in selected_tags:
                if TagModel.query.get(tag):
                    quote.tags.append(TagModel.query.get(tag))
                    flash(tag)
                else:
                    try: 
                        flash(tag)
                        newTag = TagModel(**{"name":tag})
                        db.session.add(newTag)
                        db.session.commit()
                        quote.tags.append(newTag)
                        flash("yes")
                    except:
                        db.session.rollback()
                    finally:
                        db.session.close()

            #flash() 
            try:
                db.session.add(quote)
                db.session.commit()
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
                    tags = tags,
                    quotes = quotes
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
        flash("oops")
        return render_template("add_quote.html",
            person_id = person_id,
            tag = tag,
            quote = quote,
            source = source,
            form = form,
            persons = persons,
            tags = tags,
            quotes = quotes
        )
