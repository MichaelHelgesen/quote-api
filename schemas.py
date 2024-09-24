from marshmallow import Schema, fields

class PlainQuoteSchema(Schema):
    id = fields.Str(dump_only=True)
    quote = fields.Str(required=True)
    source = fields.Str()

class PlainPersonSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class QuoteUpdateSchema(Schema):
    quote = fields.Str()
    source = fields.Str()

class QuoteSchema(PlainQuoteSchema):
    person_id = fields.Int(required=True, load_only=True)
    person = fields.Nested(PlainPersonSchema(), dump_only=True)

class PersonSchema(PlainPersonSchema):
    quotes = fields.List(fields.Nested(PlainQuoteSchema()), dump_only=True)
