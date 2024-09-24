import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import quotes
from schemas import QuoteSchema, QuoteUpdateSchema

blp = Blueprint("Quotes", __name__, description="Operations on quotes")

@blp.route("/quote/<string:quote_id>")
class Quote(MethodView):
    @blp.response(200, QuoteSchema)
    def get(self, quote_id):
        try:
            return quotes[quote_id]
        except KeyError:
            abort(404, message = "Quote not found")

    def delete(self, quote_id):
        try:
            del quotes[quote_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")
    
    @blp.arguments(QuoteUpdateSchema)
    @blp.response(200, QuoteSchema)
    def put(self, quote_data, quote_id):

        try:
            quote = quotes[quote_id]
            quote |= quote_data

            return quote
        except KeyError:
            abort(404, message="Quote not found")

@blp.route("/quote")
class QuoteList(MethodView):
    @blp.response(200, QuoteSchema(many=True))
    def get(self):
        return quotes.values()
    
    @blp.arguments(QuoteSchema)
    @blp.response(201, QuoteSchema)
    def post(self, quote_data):
            
        if quote_data["person_id"] not in persons:
            abort(404, message = "Person not found")

        quote_id = uuid.uuid4().hex
        new_quote = {**quote_data, "id": quote_id}
        quotes[quote_id] = new_quote
        
        return new_quote, 201
