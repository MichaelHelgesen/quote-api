import uuid
from flask import request, render_template, flash
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import QuoteModel
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import QuoteSchema, QuoteUpdateSchema
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class QuoteForm(FlaskForm):
    person_id = StringField("Person ID", validators=[DataRequired()])
    quote = StringField("Quote", validators=[DataRequired()])
    source = StringField("Source")
    submit = SubmitField("Submit")

class UpdateQuoteForm(FlaskForm):
    quote_id = StringField("Quote ID", validators=[DataRequired()])
    quote = StringField("Quote", validators=[DataRequired()])
    source = StringField("Source")
    submit = SubmitField("Submit")

class DeleteQuoteForm(FlaskForm):
    quote_id = StringField("Quote ID", validators=[DataRequired()])
    submit = SubmitField("Submit")

blp = Blueprint("Quotes", __name__, description="Operations on quotes")

@blp.route("/quote/<string:quote_id>")
class Quote(MethodView):
    @blp.response(200, QuoteSchema)
    def get(self, quote_id):
        quote = QuoteModel.query.get_or_404(quote_id)
        return quote

    def delete(self, quote_id):
        quote = QuoteModel.query.get_or_404(quote_id)
        db.session.delete(quote)
        db.session.commit()
        return {"message": "Quote deleted"}
    
    @blp.arguments(QuoteUpdateSchema)
    @blp.response(200, QuoteSchema)
    def put(self, quote_data, quote_id):
        quote = QuoteModel.query.get(quote_id)
        if quote:
            quote.quote = quote_data["quote"]
            quote.source = quote_data["source"]
        else:
            quote = QuoteModel(id=quote_id, **quote_data)

        db.session.add(quote)
        db.session.commit()

        return quote

@blp.route("/quote")
class QuoteList(MethodView):
    @blp.response(200, QuoteSchema(many=True))
    def get(self):
        return QuoteModel.query.all()
    
    @blp.arguments(QuoteSchema)
    @blp.response(201, QuoteSchema)
    def post(self, quote_data):
        quote = QuoteModel(**quote_data)
        
        try:
            db.session.add(quote)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured")


        return quote, 201

@blp.route("/add_quote", methods=["GET", "POST"])
def add_quote():
    person_id = None
    quote = None
    source = None
    form = QuoteForm()
    if form.validate_on_submit():
        quote = QuoteModel(**{"person_id":form.data["person_id"], "quote":form.data["quote"], "source":form.data["source"]})
        try:
            db.session.add(quote)
            db.session.commit()
            form.person_id.data = ""
            form.quote.data = ""
            form.source.data = ""
            flash("Quote added")
            return render_template("add_quote.html",
                person_id = person_id,
                quote = quote,
                source = source,
                form = form
            )
        except SQLAlchemyError:
            flash("Quote exists")
            return render_template("add_quote.html",
                person_id = person_id,
                quote = quote,
                source = source,
                form = form
            )
    return render_template("add_quote.html",
        person_id = person_id,
        quote = quote,
        source = source,
        form = form
    )

@blp.route("/update_quote", methods=["GET", "POST"])
def upd_quote():
    quote_id = None
    quote = None
    source = None
    form = UpdateQuoteForm()
    if form.validate_on_submit():
        quote = QuoteModel.query.get(form.quote_id.data)
        if quote:
            quote.quote = form.quote.data
            quote.source = form.source.data
            db.session.add(quote)
            db.session.commit()
            flash("Quote updated")
            form.quote_id.data = ""
            form.quote.data = ""
            form.source.data = ""
            return render_template("update_quote.html",
                quote_id = quote_id,
                quote = quote,
                source = source,
                form = form
            )
        else:
            quote = QuoteModel(id=quote_id, **{"quote":form.data["quote"], "source":form.data["source"]})
            flash("No quote with that ID")
            return render_template("update_quote.html",
                quote_id = quote_id,
                quote = quote,
                source = source,
                form = form
            )
    return render_template("update_quote.html",
        quote_id = quote_id,
        quote = quote,
        source = source,
        form = form
    )


@blp.route("/delete_quote", methods=["GET", "POST", "DELETE"])
def del_quote():
    quote_id = None
    form = DeleteQuoteForm()
    if form.validate_on_submit():
        quote = QuoteModel.query.get(form.quote_id.data)
        try:
            db.session.delete(quote)
            db.session.commit()
            form.quote_id.data = ""
            flash("Quote deleted")
            return render_template("delete_quote.html",
                quote_id = quote_id,
                form = form
            )
        except SQLAlchemyError:
            flash("Quote not found")
            return render_template("delete_quote.html",
                quote_id = quote_id,
                form = form
            )

    return render_template("delete_quote.html",
        quote_id = quote_id,
        form = form
        )
