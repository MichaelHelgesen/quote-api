from flask import request, render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import QuoteModel, TagModel, PersonModel 
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import QuoteSchema, QuoteUpdateSchema
from forms import QuoteForm


blp = Blueprint("Author", __name__, description="See quotes from person")

@blp.route("/author/<int:id>")
class QuoteByAuthor(MethodView):
    def get(self, id):
        persona = PersonModel.query.get_or_404(id)
        quotes = QuoteModel.query.filter(QuoteModel.person.has(id=id))
        return render_template("quote_author.html", persona = persona, quotes = quotes)
