from flask import request, render_template, flash
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import QuoteModel, TagModel
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import QuoteSchema, QuoteUpdateSchema
from forms import QuoteForm


blp = Blueprint("Homepage", __name__, description="Operations on quotes")

@blp.route("/", methods=["GET", "POST"])
def add_quote():
    person_id = None
    quote = None
    source = None
    tag = None
    form = QuoteForm()
    if form.validate_on_submit():
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
    return render_template("add_quote.html",
        person_id = person_id,
        tag = tag,
        quote = quote,
        source = source,
        form = form
    )

