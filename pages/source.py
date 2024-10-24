from flask import request, render_template, flash, redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import QuoteModel, TagModel, PersonModel 
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import QuoteSchema, QuoteUpdateSchema
from forms import QuoteForm


blp = Blueprint("Source", __name__, description="See quotes from source")

@blp.route("/source/<string:id>")
class QuoteBySource(MethodView):
    def get(self, id):
        # tag = TagModel.query.get_or_404(id)
        quotes = QuoteModel.query.filter(QuoteModel.source == id)
        return render_template("quote_source.html", quotes = quotes)

