import uuid
from flask import request, render_template, flash
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, TagAndQuoteSchema
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
'''
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, quote_id):
        if TagModel.query.filter(TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag withat that name already exists in this quote")

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
'''
@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(202, description="Deletes a tag if no item is tagged with it", example={"message":"Tag deleted"})
    @blp.alt_response(404, description="No tag found")
    @blp.alt_response(400, description="Returned if tag assigned to one or more quotes. Not deleted.")
    
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.quote:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        abort(400, message={"Could not delete tag"})

@blp.route("/tag")
class Tag(MethodView):
    @blp.response(201, TagSchema(many=True))
    def get(self):
        return TagModel.query.all()

@blp.route("/quote/<string:quote_id>/tag/<string:tag_id>")
class LinkTagsToQuotes(MethodView):
    @blp.response(201, TagSchema)
    def post(self, quote_id, tag_id):
        quote = QuoteModel.query.get_or_404(quote_id)
        tag = TagModel.query.get_or_404(tag_id)

        quote.tags.append(tag)

        try:
            db.session.add(quote)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured"),

        return tag

    @blp.response(201, TagAndQuoteSchema)
    def delete(self, quote_id, tag_id):
        quote = QuoteModel.query.get_or_404(quote_id)
        tag = TagModel.query.get_or_404(tag_id)

        quote.tags.remove(tag)

        try:
            db.session.add(quote)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured"),

        return {"message": "Tag removed from quote"}

