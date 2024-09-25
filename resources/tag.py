import uuid
from flask import request, render_template, flash
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import QuoteModel, TagModel
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

blp = Blueprint("Tags", __name__, description="Operations on tags")

@blp.route("/quote/<string:quote_id>/tag")
class TagsOnQuote(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, quote_id):
        quote = QuoteModel.query.get_or_404(quote_id)
        
        return quote.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, quote_id):
        tag = TagModel(**tag_data, quote_id=quote_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort (
                500,
                message=str(e)
                    )

        return tag

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

@blp.route("/tag")
class Tag(MethodView):
    @blp.response(201, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()
