import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import quotes

blp = Blueprint("Quotes", __name__, description="Operations on quotes")

@blp.route("/quote/<string:quote_id>")
class Quote(MethodView):
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

    def put(self, quote_id):
        quote_data = request.get_json()
        if "quote" not in quote_data or quote_data["quote"] == "":
            abort(400, message="Bad request. Ensure quote is written")

        try:
            quote = quotes[quote_id]
            quote |= quote_data

            return quote
        except KeyError:
            abort(404, message="Quote not found")

@blp.route("/quote")
class QuoteList(MethodView):
    def get(self):
        return {"quotes": list(quotes.values())}
    
    def post(self):
        quote_data = request.get_json()
        if ("quote" not in quote_data or "person_id" not in quote_data):
            abort(400, message="Bad request. Ensure 'quote' and 'person_id' are included in the JSON payload")
            
        if quote_data["person_id"] not in persons:
            abort(404, message = "Person not found")

        quote_id = uuid.uuid4().hex
        new_quote = {**quote_data, "id": quote_id}
        quotes[quote_id] = new_quote
        
        return new_quote, 201
